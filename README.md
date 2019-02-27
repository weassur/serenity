[![Build Status](https://travis-ci.org/weassur/serenity.svg?branch=master)](https://travis-ci.org/weassur/serenity)
[![codecov](https://codecov.io/gh/weassur/serenity/branch/master/graph/badge.svg)](https://codecov.io/gh/weassur/serenity)

# Serenity

Python client for the serenity api

# Usage

You'll need to get an `anonymous_token` from Serenity to authenticate.

```
from serenity.serenity import Serenity

anonymous_token = os.environ.get('SERENITY_ANONYMOUS_TOKEN')
## choose to use the production or the development endpoints
production = True

serenity_client = Serenity(anonymous_token=anonymous_token, production=production)
serenity_client.authenticate()

print(serenity_client.list_activities())

```

# Tests

intall requirements.txt

`pip install -r requirements.txt`

run tests

`py.tests`

watch for changes

`ptw -- --testmon`
