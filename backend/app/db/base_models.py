"""Import semua model agar terdaftar di Base.metadata (untuk Alembic autogen)."""
from app.db.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.business import Business  # noqa: F401
from app.models.business_configuration import BusinessConfiguration  # noqa: F401
from app.models.business_target import BusinessTarget  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.product_cost import ProductCost  # noqa: F401
from app.models.sales_transaction import SalesTransaction, SalesTransactionItem  # noqa: F401
from app.models.inventory_item import InventoryItem  # noqa: F401
from app.models.inventory_movement import InventoryMovement  # noqa: F401
from app.models.operating_expense import OperatingExpense  # noqa: F401
from app.models.forecast_result import ForecastResult  # noqa: F401
from app.models.restock_recommendation import RestockRecommendation  # noqa: F401
from app.models.pricing_recommendation import PricingRecommendation  # noqa: F401
from app.models.business_health_assessment import BusinessHealthAssessment  # noqa: F401
from app.models.growth_recommendation import GrowthRecommendation  # noqa: F401
from app.models.decision_applied import DecisionApplied  # noqa: F401
from app.models.ai_conversation import AIConversation, AIMessage  # noqa: F401
