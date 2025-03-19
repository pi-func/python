# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2025-03-19

### Added
- Initial release of PIfunc with multi-protocol support
- Core service decorator implementation for HTTP, gRPC, MQTT, WebSocket, and GraphQL protocols
- CLI tool for service management and interaction
- Type-safe function exposure across protocols
- Hot reload capability for development
- Automatic API documentation generation
- Protocol-specific configuration options
- Example implementations and usage guides
- Development tools and scripts:
  - Pre-commit hooks for code quality
  - Test automation scripts
  - Version management utilities
  - Build and publish workflows

### Changed
- Updated project structure for better modularity
- Enhanced HTTP and MQTT adapters with improved error handling
- Refined CLI interface for better user experience

### Documentation
- Added comprehensive README with installation and usage guides
- Included detailed API documentation
- Added contribution guidelines
- Created example code snippets for common use cases

### Testing
- Added comprehensive test suite:
  - CLI functionality tests
  - Service decorator tests
  - HTTP adapter tests
  - Integration tests across protocols
- Implemented test fixtures and utilities
- Added async testing support
- Added cross-protocol testing scenarios
