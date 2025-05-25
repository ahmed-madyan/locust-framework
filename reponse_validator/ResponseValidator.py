from typing import Any, Dict, List, Optional, Union, Callable
from locust.clients import HttpSession
import json
from dataclasses import dataclass
from enum import Enum
from jsonschema import validate
from logger import logger

class ValidationType(Enum):
    STATUS_CODE = "status_code"
    HEADER = "header"
    JSON_PATH = "json_path"
    JSON_SCHEMA = "json_schema"
    CUSTOM = "custom"

@dataclass
class ValidationResult:
    is_valid: bool
    message: str
    expected: Any
    actual: Any
    validation_type: ValidationType

class ResponseValidator:
    def __init__(self):
        """Initialize the ResponseValidator."""
        self._validations: List[Dict[str, Any]] = []
        self._custom_validators: Dict[str, Callable] = {}
        logger.debug("ResponseValidator initialized")

    def expect_status_code(self, status_code: Union[int, List[int]]) -> 'ResponseValidator':
        """
        Add status code validation.
        
        Args:
            status_code: Expected status code or list of acceptable status codes
        """
        self._validations.append({
            'type': ValidationType.STATUS_CODE,
            'expected': status_code
        })
        logger.debug("Status code validation added", expected=status_code)
        return self

    def expect_header(self, header_name: str, expected_value: str) -> 'ResponseValidator':
        """
        Add header validation.
        
        Args:
            header_name: Name of the header to validate
            expected_value: Expected header value
        """
        self._validations.append({
            'type': ValidationType.HEADER,
            'header_name': header_name,
            'expected': expected_value
        })
        logger.debug("Header validation added", header=header_name, expected=expected_value)
        return self

    def expect_json_path(self, json_path: str, expected_value: Any) -> 'ResponseValidator':
        """
        Add JSON path validation.
        
        Args:
            json_path: JSON path expression (e.g., 'data.user.name')
            expected_value: Expected value at the JSON path
        """
        self._validations.append({
            'type': ValidationType.JSON_PATH,
            'path': json_path,
            'expected': expected_value
        })
        logger.debug("JSON path validation added", path=json_path)
        return self

    def expect_json_schema(self, schema: Dict[str, Any]) -> 'ResponseValidator':
        """
        Add JSON schema validation.
        
        Args:
            schema: JSON schema to validate against
        """
        self._validations.append({
            'type': ValidationType.JSON_SCHEMA,
            'schema': schema
        })
        logger.debug("JSON schema validation added")
        return self

    def add_custom_validator(self, name: str, validator_func: Callable[[HttpSession], bool]) -> 'ResponseValidator':
        """
        Add a custom validation function.
        
        Args:
            name: Name of the custom validator
            validator_func: Function that takes a response and returns a boolean
        """
        self._custom_validators[name] = validator_func
        self._validations.append({
            'type': ValidationType.CUSTOM,
            'name': name
        })
        logger.debug("Custom validator added", name=name)
        return self

    def validate(self, response: HttpSession) -> List[ValidationResult]:
        """
        Validate the response against all configured validations.
        
        Args:
            response: The response to validate
            
        Returns:
            List of validation results
        """
        logger.info("Starting response validation", 
                   status_code=response.status_code,
                   validation_count=len(self._validations))
        
        results = []
        
        for validation in self._validations:
            validation_type = validation['type']
            
            if validation_type == ValidationType.STATUS_CODE:
                expected = validation['expected']
                actual = response.status_code
                is_valid = actual == expected if isinstance(expected, int) else actual in expected
                result = ValidationResult(
                    is_valid=is_valid,
                    message=f"Status code validation failed. Expected {expected}, got {actual}",
                    expected=expected,
                    actual=actual,
                    validation_type=validation_type
                )
                results.append(result)
                logger.debug("Status code validation result", 
                           is_valid=is_valid,
                           expected=expected,
                           actual=actual)
                
            elif validation_type == ValidationType.HEADER:
                header_name = validation['header_name']
                expected = validation['expected']
                actual = response.headers.get(header_name)
                is_valid = actual == expected
                result = ValidationResult(
                    is_valid=is_valid,
                    message=f"Header validation failed for {header_name}. Expected {expected}, got {actual}",
                    expected=expected,
                    actual=actual,
                    validation_type=validation_type
                )
                results.append(result)
                logger.debug("Header validation result", 
                           header=header_name,
                           is_valid=is_valid,
                           expected=expected,
                           actual=actual)
                
            elif validation_type == ValidationType.JSON_PATH:
                try:
                    path = validation['path']
                    expected = validation['expected']
                    response_json = response.json()
                    # Implement JSON path validation logic here
                    actual = None  # Get actual value from JSON path
                    is_valid = actual == expected
                    result = ValidationResult(
                        is_valid=is_valid,
                        message=f"JSON path validation failed for {path}. Expected {expected}, got {actual}",
                        expected=expected,
                        actual=actual,
                        validation_type=validation_type
                    )
                    results.append(result)
                    logger.debug("JSON path validation result", 
                               path=path,
                               is_valid=is_valid,
                               expected=expected,
                               actual=actual)
                except Exception as e:
                    result = ValidationResult(
                        is_valid=False,
                        message=f"JSON path validation failed: {str(e)}",
                        expected=validation['expected'],
                        actual=None,
                        validation_type=validation_type
                    )
                    results.append(result)
                    logger.error("JSON path validation error", 
                               path=validation['path'],
                               error=str(e))
                    
            elif validation_type == ValidationType.JSON_SCHEMA:
                try:
                    response_json = response.json()
                    schema = validation['schema']
                    validate(instance=response_json, schema=schema)
                    result = ValidationResult(
                        is_valid=True,
                        message="JSON schema validation passed",
                        expected=schema,
                        actual=response_json,
                        validation_type=validation_type
                    )
                    results.append(result)
                    logger.debug("JSON schema validation passed")
                except Exception as e:
                    result = ValidationResult(
                        is_valid=False,
                        message=f"JSON schema validation failed: {str(e)}",
                        expected=schema,
                        actual=response.json() if hasattr(response, 'json') else None,
                        validation_type=validation_type
                    )
                    results.append(result)
                    logger.error("JSON schema validation failed", error=str(e))
                    
            elif validation_type == ValidationType.CUSTOM:
                validator_name = validation['name']
                if validator_name in self._custom_validators:
                    validator_func = self._custom_validators[validator_name]
                    is_valid = validator_func(response)
                    result = ValidationResult(
                        is_valid=is_valid,
                        message=f"Custom validation '{validator_name}' {'passed' if is_valid else 'failed'}",
                        expected="Custom validation to pass",
                        actual="Custom validation result",
                        validation_type=validation_type
                    )
                    results.append(result)
                    logger.debug("Custom validation result", 
                               name=validator_name,
                               is_valid=is_valid)
        
        failed_count = len([r for r in results if not r.is_valid])
        logger.info("Validation completed", 
                   total_validations=len(results),
                   failed_validations=failed_count)
        
        return results

    def assert_valid(self, response: HttpSession) -> None:
        """
        Assert that all validations pass, raising an AssertionError if any fail.
        
        Args:
            response: The response to validate
            
        Raises:
            AssertionError: If any validation fails
        """
        results = self.validate(response)
        failed_validations = [r for r in results if not r.is_valid]
        
        if failed_validations:
            error_messages = [f"{r.validation_type.value}: {r.message}" for r in failed_validations]
            error_msg = "\n".join(error_messages)
            logger.error("Validation assertion failed", 
                        failed_count=len(failed_validations),
                        errors=error_messages)
            raise AssertionError(error_msg)
        
        logger.info("All validations passed")

    def reset(self) -> 'ResponseValidator':
        """Reset all validations."""
        self._validations = []
        self._custom_validators = {}
        logger.debug("ResponseValidator reset")
        return self 