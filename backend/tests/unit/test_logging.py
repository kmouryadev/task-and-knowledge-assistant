import structlog

from app.core.logging import configure_logging, get_logger


def test_get_logger_returns_bound_logger():
    configure_logging()
    logger = get_logger("test")
    assert isinstance(logger, structlog.stdlib.BoundLogger) or hasattr(logger, "info")


def test_configure_logging_is_idempotent():
    configure_logging()
    configure_logging()
    logger = get_logger("test")
    logger.info("smoke_test", key="value")
