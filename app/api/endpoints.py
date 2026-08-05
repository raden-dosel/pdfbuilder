from fastapi import APIRouter, Response, HTTPException, Depends
from app.models.schemas import DocumentPayload
from app.services.pdf_builder import generate_pdf_bytes
from app.core.config import settings
from app.core.security import verify_api_key
from datetime import timedelta
import logging

# Set up simple logging for production monitoring
logger = logging.getLogger("uvicorn.error")

# Dynamically apply the prefix from core/config.py instead of hardcoding it
router = APIRouter(prefix=settings.API_V1_STR, tags=["PDF Generation"])

@router.post("/invoices/generate")
async def generate_invoice(payload: DocumentPayload, _: str = Depends(verify_api_key)):
    """
    Accepts invoice data, renders it into the invoice HTML template,
    and returns a downloadable PDF byte stream.
    Requires valid API key in X-API-Key header.
    """
    try:
        # Pydantic v2 mode_dump handles the schema validation conversion cleanly
        data = payload.model_dump()
        
        # Compile PDF entirely in memory
        pdf_bytes = generate_pdf_bytes("invoice.html", {"doc": data})
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=invoice_{payload.document_id}.pdf"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate invoice {payload.document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during PDF generation.")

@router.post("/quotations/generate")
async def generate_quotation(payload: DocumentPayload, _: str = Depends(verify_api_key)):
    """
    Accepts quotation/estimate data, renders it into the quotation HTML template,
    and returns a downloadable PDF byte stream.
    Requires valid API key in X-API-Key header.
    """
    try:
        data = payload.model_dump()
        quote_number = payload.document_id if str(payload.document_id).startswith("QT-") else f"QT-{payload.document_id}"
        data.update(
            {
                "quote_number": quote_number,
                "valid_until": payload.date_issued + timedelta(days=14),
                "prepared_by": payload.sender.contact,
            }
        )
        pdf_bytes = generate_pdf_bytes("quotation.html", {"doc": data})
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=quotation_{payload.document_id}.pdf"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate quotation {payload.document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during PDF generation.")

@router.post("/receipts/generate")
async def generate_receipt(payload: DocumentPayload, _: str = Depends(verify_api_key)):
    """
    Accepts receipt data, renders it into the receipt HTML template,
    and returns a downloadable PDF byte stream.
    Requires valid API key in X-API-Key header.
    """
    try:
        data = payload.model_dump()
        pdf_bytes = generate_pdf_bytes("receipt.html", {"doc": data})
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=receipt_{payload.document_id}.pdf"
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate receipt {payload.document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during PDF generation.")