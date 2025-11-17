from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import stripe
from database import get_db
from models import User
from auth import get_current_user
from config import settings

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/subscription", tags=["Subscription"])


class CheckoutRequest(BaseModel):
    plan: str  # weekly, monthly, yearly


class PortalRequest(BaseModel):
    return_url: str


@router.post("/create-checkout-session")
async def create_checkout_session(
    checkout_request: CheckoutRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a Stripe checkout session"""
    # Define price IDs (you'll need to create these in Stripe Dashboard)
    price_ids = {
        "weekly": "price_weekly_399",  # Replace with actual Stripe price ID
        "monthly": "price_monthly_999",  # Replace with actual Stripe price ID
        "yearly": "price_yearly_4900"  # Replace with actual Stripe price ID
    }

    price_id = price_ids.get(checkout_request.plan)
    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid plan")

    try:
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='studyhero://subscription/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='studyhero://subscription/cancel',
            metadata={
                'user_id': str(current_user.id),
                'plan': checkout_request.plan
            }
        )

        return {
            "session_id": checkout_session.id,
            "url": checkout_session.url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-portal-session")
async def create_portal_session(
    portal_request: PortalRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a Stripe customer portal session"""
    if not current_user.subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription")

    try:
        # Get customer from subscription
        subscription = stripe.Subscription.retrieve(current_user.subscription_id)
        customer_id = subscription.customer

        # Create portal session
        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=portal_request.return_url,
        )

        return {
            "url": portal_session.url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = int(session['metadata']['user_id'])
        subscription_id = session['subscription']

        # Update user subscription
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.subscription_status = "premium"
            user.subscription_id = subscription_id

            # Set expiration based on plan
            plan = session['metadata']['plan']
            if plan == 'weekly':
                user.subscription_expires_at = datetime.utcnow() + timedelta(days=7)
            elif plan == 'monthly':
                user.subscription_expires_at = datetime.utcnow() + timedelta(days=30)
            elif plan == 'yearly':
                user.subscription_expires_at = datetime.utcnow() + timedelta(days=365)

            db.commit()

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        subscription_id = subscription['id']

        # Update subscription status
        user = db.query(User).filter(User.subscription_id == subscription_id).first()
        if user:
            if subscription['status'] == 'active':
                user.subscription_status = "premium"
                # Update expiration date
                user.subscription_expires_at = datetime.fromtimestamp(subscription['current_period_end'])
            else:
                user.subscription_status = "free"

            db.commit()

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        subscription_id = subscription['id']

        # Cancel subscription
        user = db.query(User).filter(User.subscription_id == subscription_id).first()
        if user:
            user.subscription_status = "free"
            user.subscription_expires_at = None
            user.subscription_id = None
            db.commit()

    return {"status": "success"}


@router.get("/status")
async def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    """Get current subscription status"""
    is_premium = False
    expires_at = None

    # Check premium subscription
    if current_user.subscription_status == "premium":
        if current_user.subscription_expires_at and current_user.subscription_expires_at > datetime.utcnow():
            is_premium = True
            expires_at = current_user.subscription_expires_at

    # Check trial
    in_trial = False
    trial_ends_at = None
    if not current_user.trial_used and current_user.trial_ends_at:
        if current_user.trial_ends_at > datetime.utcnow():
            in_trial = True
            trial_ends_at = current_user.trial_ends_at

    return {
        "subscription_status": current_user.subscription_status,
        "is_premium": is_premium or in_trial,
        "in_trial": in_trial,
        "trial_ends_at": trial_ends_at.isoformat() if trial_ends_at else None,
        "subscription_expires_at": expires_at.isoformat() if expires_at else None
    }


@router.get("/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    return {
        "plans": [
            {
                "id": "weekly",
                "name": "Weekly",
                "price": 3.99,
                "currency": "USD",
                "interval": "week",
                "features": [
                    "Unlimited homework scans",
                    "Advanced explanations",
                    "Unlimited quizzes",
                    "AI tutor chat",
                    "Priority support"
                ]
            },
            {
                "id": "monthly",
                "name": "Monthly",
                "price": 9.99,
                "currency": "USD",
                "interval": "month",
                "features": [
                    "Unlimited homework scans",
                    "Advanced explanations",
                    "Unlimited quizzes",
                    "AI tutor chat",
                    "Priority support",
                    "Save 17% vs weekly"
                ]
            },
            {
                "id": "yearly",
                "name": "Yearly",
                "price": 49.00,
                "currency": "USD",
                "interval": "year",
                "features": [
                    "Unlimited homework scans",
                    "Advanced explanations",
                    "Unlimited quizzes",
                    "AI tutor chat",
                    "Priority support",
                    "Save 60% vs monthly",
                    "Best value!"
                ]
            }
        ],
        "free_trial_days": 3
    }
