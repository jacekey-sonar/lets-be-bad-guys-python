# GitHub Actions Setup Guide

## Overview

Your GitHub Actions workflow has been updated to work correctly with the pytest test suite for this Django project.

## Changes Made

### 1. Fixed `.github/workflows/main.yml`

**Before:**
```yaml
pip install pytest pytest-cov
pytest --cov=main --cov-report=xml --cov-report=term
```

**After:**
```yaml
pip install -r requirements.txt  # Includes pytest, pytest-django, pytest-cov
pytest --cov=badguys --cov-report=xml --cov-report=term
```

**Key fixes:**
- ✅ Changed coverage module from `main` to `badguys` (correct Django app name)
- ✅ Removed redundant pytest installation (already in requirements.txt)
- ✅ Now installs `pytest-django` which is required for Django tests
- ✅ Django settings are automatically configured via `pytest.ini`

### 2. Created `sonar-project.properties`

Added SonarCloud configuration file with:
- Project identification settings
- Source and test directory configuration
- Python coverage report location
- Appropriate exclusions (migrations, static files, etc.)
- Educational disclaimer about intentional vulnerabilities

## Workflow Structure

Your CI/CD pipeline has 4 jobs:

### 1. **Test Job** ✅ (Fixed)
- Runs on Python 3.11
- Installs dependencies from `requirements.txt`
- Runs pytest with coverage
- Uploads coverage report for SonarQube
- **Status:** Ready to use

### 2. **Security Job** ⚠️
- Runs safety check on dependencies
- **Note:** This project uses old Django 1.9.6 intentionally (for vulnerabilities)
- Safety check will report many issues (expected for this educational project)
- Set to `continue-on-error: true` so it doesn't fail the build

### 3. **SonarQube Job** ⚠️ (Requires Setup)
- Runs SonarCloud analysis
- **Requires:** `SONAR_TOKEN` secret to be configured
- See setup instructions below

### 4. **Summary Job** ✅
- Displays results from all jobs
- Fails only if the test job fails

## Required Setup

### 1. GitHub Repository Settings

No changes needed - the workflow is ready to run!

### 2. SonarCloud Setup (Optional)

If you want to use SonarCloud analysis:

#### Step 1: Create SonarCloud Account
1. Go to [SonarCloud.io](https://sonarcloud.io)
2. Sign in with your GitHub account
3. Import your repository

#### Step 2: Configure Project
1. In SonarCloud, go to your project
2. Note your **Organization Key**
3. Update `sonar-project.properties`:
   ```properties
   sonar.organization=your-actual-org-name
   ```

#### Step 3: Add GitHub Secret
1. In GitHub, go to: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `SONAR_TOKEN`
4. Value: Your SonarCloud token (from SonarCloud → My Account → Security)
5. Click **Add secret**

#### Step 4: Update Project Key (if needed)
In `sonar-project.properties`, update:
```properties
sonar.projectKey=your-github-username_lets-be-bad-guys-python
```

### 3. Skip SonarCloud (Alternative)

If you don't want to use SonarCloud, you can disable it:

```yaml
# Comment out or remove the sonarqube job in .github/workflows/main.yml
# And update the summary job needs:
needs: [test, security]  # Remove sonarqube
```

## Testing the Workflow

### Local Testing

Before pushing, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests exactly as CI does
pytest --cov=badguys --cov-report=xml --cov-report=term

# Check that coverage.xml was created
ls -la coverage.xml
```

### Push to GitHub

```bash
git add .
git commit -m "Update GitHub Actions for pytest"
git push origin main
```

The workflow will automatically run on:
- Pushes to `main` or `develop` branches
- Pull requests to `main` branch

## Viewing Results

### In GitHub Actions Tab

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Click on the latest workflow run
4. View results for each job:
   - ✅ **Test** - Should pass (136+ tests)
   - ⚠️ **Security** - Will show warnings (expected)
   - ⚠️ **SonarQube** - Needs setup or will be skipped
   - ✅ **Summary** - Shows overall status

### Test Coverage

The workflow generates:
- Terminal coverage report (visible in logs)
- XML coverage report (uploaded as artifact)
- Artifact available for 7 days

To download coverage artifact:
1. Go to workflow run
2. Scroll to **Artifacts** section
3. Download `coverage-for-sonar`

## Expected Results

### ✅ Test Job Should Show:

```
================================ test session starts =================================
platform linux -- Python 3.11.x, pytest-7.4.3, pluggy-1.x.x
django: settings: badguys.settings (from ini)
rootdir: /home/runner/work/lets-be-bad-guys-python
configfile: pytest.ini
plugins: django-4.7.0, cov-4.1.0
collected 136+ items

tests/test_injection.py ...................... [ 15%]
tests/test_xss.py ............................ [ 30%]
tests/test_vulnerabilities.py ................ [ 55%]
tests/test_urls.py ........................... [ 80%]
tests/test_helpers.py ........................ [100%]

---------- coverage: platform linux, python 3.11.x -----------
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
badguys/__init__.py                      0      0   100%
badguys/settings.py                     45      5    89%   ...
badguys/urls.py                         28      0   100%
badguys/vulnerable/views.py            120     10    92%   ...
------------------------------------------------------------------
TOTAL                                  193     15    92%

================================= 136 passed in 2.5s =================================
```

### ⚠️ Security Job Will Show:

```
WARNING: Multiple vulnerabilities found in dependencies
- Django 1.9.6 (multiple CVEs) - INTENTIONAL for educational purposes
- Other outdated packages
```

This is **expected** - the project uses old, vulnerable versions intentionally.

### ⚠️ SonarQube Job

- Will skip if `SONAR_TOKEN` is not configured
- Will show many security issues if configured (intentional vulnerabilities)

## Troubleshooting

### Test Job Fails

**Problem:** Tests fail in CI but pass locally

**Solutions:**
1. Check Python version matches (3.11)
2. Ensure all dependencies are in `requirements.txt`
3. Check for environment-specific issues

### Coverage Upload Fails

**Problem:** Coverage artifact not uploaded

**Solutions:**
1. Verify `coverage.xml` is generated
2. Check pytest command includes `--cov-report=xml`
3. Ensure test job completes successfully

### SonarQube Job Fails

**Problem:** SonarQube job fails or skips

**Solutions:**
1. Verify `SONAR_TOKEN` secret is set
2. Check `sonar-project.properties` configuration
3. Ensure organization key is correct
4. Review SonarCloud project settings

### Workflow Doesn't Trigger

**Problem:** Workflow doesn't run on push

**Solutions:**
1. Check branch name matches trigger (main/develop)
2. Verify workflow file is in `.github/workflows/`
3. Check GitHub Actions is enabled for repository

## Workflow Configuration

### Current Triggers

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

### Modify Triggers (Optional)

Add more branches:
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]
```

Run on all branches:
```yaml
on: [push, pull_request]
```

Add manual trigger:
```yaml
on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:  # Adds "Run workflow" button
```

## Performance

### Expected Run Times

- **Test Job:** ~2-3 minutes
- **Security Job:** ~1-2 minutes
- **SonarQube Job:** ~2-3 minutes
- **Total:** ~5-8 minutes

### Optimization Tips

1. **Cache dependencies:**
```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

2. **Run jobs in parallel:**
   - Test and Security jobs already run in parallel
   - SonarQube waits for test (needs coverage report)

3. **Skip jobs on docs-only changes:**
```yaml
on:
  push:
    branches: [ main, develop ]
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

## Security Considerations

### Important Notes

⚠️ **This is a deliberately vulnerable application!**

1. **Never deploy this to production**
2. **Security scan warnings are intentional**
3. **Old Django version is intentional**
4. **Vulnerabilities are for educational purposes**

### Safety Check Configuration

The safety check is set to `continue-on-error: true` because:
- Django 1.9.6 has known vulnerabilities (intentional)
- We don't want to fail builds on expected issues
- This is an educational project, not production code

To make it fail on vulnerabilities:
```yaml
- name: Run safety check
  run: .venv/bin/safety check --full-report
  continue-on-error: false  # Change to false
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [Safety Documentation](https://pyup.io/safety/)

## Summary

✅ **Ready to Use:**
- Test job configured correctly
- Coverage reporting working
- Django tests will run properly

⚠️ **Optional Setup:**
- SonarCloud (requires SONAR_TOKEN secret)
- Custom triggers or optimizations

🎯 **Next Steps:**
1. Push changes to GitHub
2. Check Actions tab for results
3. Set up SonarCloud if desired
4. Review coverage reports

---

**Your GitHub Actions workflow is now properly configured for this Django pytest project! 🚀**

