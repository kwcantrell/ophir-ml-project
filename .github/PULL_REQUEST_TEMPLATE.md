---
name: PR Template
about: Create a pull request from feature branches to main
labels: []
assignees: ''

---

## 📝 Description

<!-- Describe the changes in this PR and link to any related issues -->
- [ ] Fixes issue/PR #___
- [ ] Addresses problem/solves use case described below


## Type of Change

<!-- What kind of change does this PR introduce? -->
- [ ] `feat` - New feature (non-breaking)
- [ ] `fix` - Bug fix
- [ ] `docs` - Documentation only
- [ ] `style` - Code style/formatting changes
- [ ] `refactor` - Code reorganization, no logic change
- [ ] `perf` - Performance improvement
- [ ] `test` - Adding tests
- [ ] `chore` - Maintenance tasks (config, deps)
- [ ] `ci` - CI/CD configuration changes


## Testing

<!-- Describe testing done: manual tests, automated tests run -->
- [ ] Tests added/updated
- [ ] Manual testing completed
- [ ] Performance implications discussed if applicable


## Screenshots/Videos (if applicable)

<!-- Add any relevant UI/UX screenshots or video recordings here -->


## Checklist for Reviewers

- [ ] Code follows existing patterns in the codebase
- [ ] No sensitive information exposed (keys, secrets, PII)
- [ ] Tests cover happy path and edge cases
- [ ] Error handling is complete for failure paths
- [ ] Functions kept focused and readable (avoid giant functions)
- [ ] Related issues referenced in commit messages
- [ ] Breaking changes documented with clear migration path


## Breaking Changes

<!-- If this PR introduces breaking changes, describe them here -->

**Before:**
```code-before-change-section
Description of how the system worked before
```

**After:**
```code-after-change-section
Description of how the system works after
```

**Migration:**
```migration-steps
Step-by-step instructions for migrating to new behavior
```
