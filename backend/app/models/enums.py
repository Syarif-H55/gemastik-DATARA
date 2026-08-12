"""Enumerasi bersama untuk model DATARA.

Nilai mengikuti DATA_DICTIONARY_AND_DATA_MODEL_DATARA.md (FINAL).
"""
import enum


class MovementType(str, enum.Enum):
    RESTOCK = "RESTOCK"
    SALE = "SALE"
    ADJUSTMENT = "ADJUSTMENT"
    WASTE = "WASTE"


class TargetType(str, enum.Enum):
    SALES = "SALES"
    PROFIT = "PROFIT"


class PeriodType(str, enum.Enum):
    MONTHLY = "MONTHLY"


class TargetStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CostType(str, enum.Enum):
    RAW_MATERIAL = "RAW_MATERIAL"
    PACKAGING = "PACKAGING"
    DIRECT_LABOR = "DIRECT_LABOR"
    PRODUCTION_OVERHEAD = "PRODUCTION_OVERHEAD"


class TransactionStatus(str, enum.Enum):
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ExpenseType(str, enum.Enum):
    RENT = "RENT"
    FIXED_SALARY = "FIXED_SALARY"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    OTHER = "OTHER"


class RecommendationStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DISMISSED = "DISMISSED"
    EXPIRED = "EXPIRED"


class HealthStatus(str, enum.Enum):
    SEHAT = "SEHAT"
    PERLU_PERHATIAN = "PERLU_PERHATIAN"
    BERISIKO = "BERISIKO"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class GrowthCategory(str, enum.Enum):
    PRICING = "PRICING"
    SALES = "SALES"
    INVENTORY = "INVENTORY"
    PROFITABILITY = "PROFITABILITY"


class GrowthPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GrowthStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DISMISSED = "DISMISSED"
    EXPIRED = "EXPIRED"


class ConversationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class MessageRole(str, enum.Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class DecisionAppliedType(str, enum.Enum):
    PRICING = "PRICING"
    RESTOCK = "RESTOCK"


class DecisionAppliedStatus(str, enum.Enum):
    IMPROVED = "IMPROVED"
    FLAT = "FLAT"
    REGRESSED = "REGRESSED"
    UNKNOWN = "UNKNOWN"
