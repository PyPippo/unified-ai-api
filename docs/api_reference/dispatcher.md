# Dispatcher API Reference

This document provides the complete API reference for the `Dispatcher` class and related dispatcher functionality.

## Class: Dispatcher

The `Dispatcher` class handles routing and management of API requests across different providers.

### Overview

The dispatcher is responsible for:

- Request routing based on API type
- Load balancing across multiple endpoints
- Failover and retry logic
- Request/response transformation

### Constructor

```python
Dispatcher(config)
```

#### Parameters

- `config` (dict): Configuration dictionary containing dispatcher settings

### Methods

#### dispatch()

Routes a request to the appropriate API handler.

#### register_handler()

Registers a new API handler with the dispatcher.

#### unregister_handler()

Removes an API handler from the dispatcher.

#### get_handler_status()

Returns the status of registered handlers.

### Configuration

#### Handler Registration

How to register custom API handlers.

#### Routing Rules

Configuration of request routing logic.

#### Failover Settings

Setting up automatic failover behavior.

### Usage Examples

```python
# Dispatcher usage examples will be added here
```

### Advanced Features

- Custom middleware integration
- Request/response logging
- Performance monitoring
- Health checks

---

*This documentation is under development. More detailed content will be added in future versions.*
