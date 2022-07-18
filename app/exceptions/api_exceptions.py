from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette import status


class BaseAPIException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    status_name = "Bad Request"
    detail = "Default exception"

    def __init__(
            self,
            status_code: int = None,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code=status_code, detail=detail, headers=headers)

    def json(self):
        return {
            'status': self.status_name,
            'code': self.status_code,
            'message': self.detail
        }


class NotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    status_name = "NOT_FOUND"
    detail = "Result not found"


class AccessDenied(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    status_name = "ACCESS_DENIED"
    detail = "Access denied"
