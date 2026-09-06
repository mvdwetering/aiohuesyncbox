# aiohuesyncbox Project Guidelines

## Code Style

- **Language**: Python 3.11+ required
- **Type hints**: All functions must be type-annotated; use `mypy` for validation
- **Formatting**: Use `ruff` with default settings for code formatting and linting
- **Async patterns**: Use `asyncio` and `aiohttp` for I/O; functions that make requests must be `async def`

## Architecture

aiohuesyncbox uses a **models/controllers split** to separate concerns:

- **Models** (`aiohuesyncbox/models/`): Pure `mashumaro` dataclasses that handle JSON deserialization/serialization with camelCase ↔ snake_case conversion. No I/O or network operations.
- **Controllers** (`aiohuesyncbox/controllers/`): Thin wrapper classes (`Resource` and `CollectionResource` subclasses) that bind a model instance + request function and add mutation/update methods.

Key patterns:

- `Resource` subclasses use `@property` methods (one per model field) for delegation and type safety — this allows `box.device.name` attribute access while maintaining type hints and IDE support.
- `TYPE_CHECKING` blocks are NOT used; all fields must be real `@property` definitions.
- Field/attribute names must match the API spec 1:1 for discoverability. If a model field name collides with a method name, rename the method (not the field).
- `HueSyncBox.refresh_data()` fetches fresh data from the device; individual resource `refresh_data()` methods update that resource.

## Build and Test

**Dependencies**: See `pyproject.toml` for runtime and test dependencies; currently requires Python 3.11+.

**Install**:

```bash
pip install -e ".[test]"
```

**Test**:

```bash
pytest  # Run all tests with asyncio_mode=auto
```

**Type check**:

```bash
mypy aiohuesyncbox
```

**Lint and format**:

```bash
ruff check aiohuesyncbox  # Check for issues
ruff format aiohuesyncbox  # Auto-format
```

**Test files**:

- `tests/test_compatibility.py`: Compatibility tests for API changes
- `tests/test_models.py`: Pure data parsing via mashumaro
- `tests/test_resource.py`: Controller behavior via `FakeRequest` (no network)

## Conventions

- **Mashumaro metadata**: Use `BaseModel.__pre_deserialize__` / `__post_serialize__` hooks in model definitions for field name mapping (camelCase JSON ↔ snake_case Python).
- **Instances vs class attrs**: Non-JSON runtime attributes (e.g., `_request` callable, resource id) must be assigned in `__post_init__` as instance attributes, not ClassVar, to avoid mashumaro serialization issues.
- **Property delegation**: All `Resource` subclass fields must be exposed as `@property` methods with correct type annotations matching the model. Go-to-definition IDE support depends on real properties, not stubs.
- **Naming model updates**: `DeviceUpdate`, `ExecutionUpdate`, etc. follow the pattern `<ResourceName>Update` for PATCH payloads; the `Resource` method to apply them is `async def refresh(payload: <ResourceName>Update)`.
- **Collection resources**: `Presets` and `Registrations` use `CollectionResource` with dict-based item indexing by id; different pattern from single-resource `__getattr__` delegation.

For more details on the mashumaro migration and type-checking evolution, see the project's internal docs.
