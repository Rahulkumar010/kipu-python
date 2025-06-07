# Kipu API Python library

A comprehensive Python library for the Kipu Healthcare API (V3) with HMAC SHA1 authentication and recursive JSON flattening capabilities.

## Features

- ✅ **Complete API Coverage**: All 80+ Kipu API V3 endpoints implemented
- 🔐 **Secure Authentication**: HMAC SHA1 signature generation
- 📊 **Automatic Flattening**: Converts nested JSON responses to pandas DataFrames
- ⚡ **Async Support**: Built with asyncio for high performance
- 🛡️ **Error Handling**: Comprehensive exception hierarchy
- 📝 **Type Hints**: Full typing support for better development experience
- 🔄 **Flexible Response Format**: Choose between raw JSON or flattened DataFrames

## Installation

```bash
# Install required dependencies
pip install aiohttp pandas numpy tqdm
```

## Quick Start

```python
import asyncio
from kipu import KipuClient

async def main():
    async with KipuClient(
        access_id="your_access_id",
        secret_key="your_secret_key", 
        app_id="your_app_id"
    ) as client:
        
        # Get patient census as flattened DataFrame
        census_df = await client.get_patients_census()
        print(f"Found {len(census_df)} patients")
        
        # Get specific patient as raw JSON
        patient_data = await client.get_patient("patient_id", flatten=False)
        print(f"Patient: {patient_data['first_name']} {patient_data['last_name']}")

asyncio.run(main())
```

## Authentication

The library handles HMAC SHA1 signature generation automatically. You need three credentials from Kipu:

- `access_id`: Your API access identifier
- `secret_key`: Your secret key for signature generation
- `app_id`: Your application ID (also called recipient_id)

## API Endpoints

### Patient Management

```python
# Get patient census
census_df = await client.get_patients_census(params={
    "phi_level": "high",
    "page": 1,
    "per": 50
})

# Get specific patient
patient = await client.get_patient("patient_id")

# Create new patient
patient_data = {
    "document": {
        "recipient_id": app_id,
        "data": {
            "first_name": "John",
            "last_name": "Doe",
            "dob": "1990-01-01",
            # ... other fields
        }
    }
}
new_patient = await client.create_patient(patient_data)

# Update patient
await client.update_patient("patient_id", updated_data)
```

### Medical Records

```python
# Get vital signs
vital_signs_df = await client.get_vital_signs()

# Get patient-specific vital signs
patient_vitals = await client.get_patient_vital_signs(
    "patient_id",
    params={
        "created_at_start_date": "2024-01-01",
        "created_at_end_date": "2024-12-31"
    }
)

# Create vital signs
vital_data = {
    "document": {
        "recipient_id": app_id,
        "data": {
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 72
        }
    }
}
await client.create_patient_vital_signs("patient_id", vital_data)

# Get allergies
allergies_df = await client.get_allergies()
patient_allergies = await client.get_patient_allergies("patient_id")
```

### Appointments

```python
# Get all appointments
appointments_df = await client.get_scheduler_appointments(params={
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
})

# Get patient appointments
patient_appointments = await client.get_patient_appointments("patient_id")

# Get appointment types and statuses
types_df = await client.get_scheduler_appointment_types()
statuses_df = await client.get_scheduler_appointment_statuses()
```

### Administrative

```python
# Get locations
locations_df = await client.get_locations(params={"include_buildings": True})

# Get users and providers
users_df = await client.get_users()
providers_df = await client.get_providers()

# Get roles
roles_df = await client.get_roles()
```

## Response Processing

### Automatic Flattening

By default, the library automatically flattens nested JSON responses into pandas DataFrames:

```python
# This returns a flattened DataFrame
census_df = await client.get_patients_census()
print(type(census_df))  # <class 'pandas.core.frame.DataFrame'>
```

### Raw JSON Response

You can get raw JSON responses by setting `flatten=False`:

```python
# This returns raw JSON
census_data = await client.get_patients_census(flatten=False)
print(type(census_data))  # <class 'dict'> or <class 'list'>
```

### Global Flattening Setting

You can disable auto-flattening globally:

```python
async with KipuClient(
    access_id, secret_key, app_id,
    auto_flatten=False
) as client:
    # All responses will be raw JSON by default
    raw_data = await client.get_patients_census()
    
    # You can still request flattening for specific calls
    flat_data = await client.get_patients_census(flatten=True)
```

## Error Handling

The library provides a comprehensive exception hierarchy:

```python
from kipu.exceptions import (
    KipuAPIError,
    KipuAuthenticationError,
    KipuValidationError,
    KipuNotFoundError,
    KipuServerError
)

try:
    patient = await client.get_patient("invalid_id")
except KipuNotFoundError as e:
    print(f"Patient not found: {e.message}")
except KipuAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except KipuAPIError as e:
    print(f"API error: {e.message} (Status: {e.status_code})")
```

## File Uploads

For endpoints that support file uploads (multipart/form-data):

```python
# Patient with attachment
patient_data = {
    "document[recipient_id]": app_id,
    "document[data][first_name]": "John",
    "document[data][last_name]": "Doe"
}

files = {
    "document[attachments_attributes][0][attachment]": {
        "content": file_bytes,
        "filename": "patient_id.jpg",
        "content_type": "image/jpeg"
    }
}

await client.create_patient(patient_data, files=files)
```

## Advanced Usage

### Custom Flattening

You can use the JsonFlattener directly for custom flattening:

```python
from kipu.flattener import JsonFlattener

flattener = JsonFlattener(sep='__')  # Custom separator
flat_data = flattener.flatten_json(your_nested_data)
```

### Pagination

Many endpoints support pagination:

```python
# Get paginated results
page_1 = await client.get_patients_census(params={"page": 1, "per": 50})
page_2 = await client.get_patients_census(params={"page": 2, "per": 50})
```

### Date Filtering

Use date parameters for time-based filtering:

```python
# Get recent patients
recent_patients = await client.get_patients_latest(params={
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
})
```

## Available Endpoints

The library covers all Kipu API V3 endpoints organized by category:

### Patients
- `get_patients_census()` - Patient census
- `get_patient()` - Individual patient
- `create_patient()` - Create patient
- `update_patient()` - Update patient
- `get_patients_admissions()` - Admissions
- `get_patients_latest()` - Recently updated patients
- `get_vaults_patients()` - Soft-deleted patients

### Medical Records
- Vital Signs: `get_vital_signs()`, `get_patient_vital_signs()`, `create_patient_vital_signs()`
- Allergies: `get_allergies()`, `get_patient_allergies()`, `get_allergens()`
- Assessments: `get_cows()`, `get_ciwa_ars()`, `get_ciwa_bs()`
- Glucose Logs: `get_glucose_logs()`, `get_patient_glucose_logs()`
- Orthostatic Vitals: `get_orthostatic_vital_signs()`

### Evaluations
- `get_evaluations()` - All evaluations
- `get_patient_evaluations()` - Patient evaluations
- `create_patient_evaluation()` - Create evaluation

### Appointments
- `get_scheduler_appointments()` - All appointments
- `get_patient_appointments()` - Patient appointments
- `get_scheduler_appointment_types()` - Appointment types
- `get_scheduler_appointment_statuses()` - Appointment statuses

### Users & Providers
- `get_users()`, `get_user()` - User management
- `get_providers()`, `get_provider()` - Provider management
- `get_roles()`, `get_user_roles()` - Role management

### Administrative
- `get_locations()` - Facility locations
- `get_care_levels()` - Levels of care
- `get_flags()`, `get_flag_categories()` - Patient flags
- `get_patient_colors()`, `get_patient_tags()` - Patient categorization

### Insurance & Billing
- `get_insurances_latest()` - Insurance records
- `update_patient_insurance()` - Update insurance

[See examples.py for complete usage examples]

## Requirements

- Python 3.8+
- aiohttp
- pandas
- numpy
- tqdm

## License

This library is provided as-is for integration with the Kipu Healthcare API.
