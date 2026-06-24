<!-- # Testing: Getting Started -->
# Testing: Getting Started

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
    - [Running Tests In Parallel](#running-tests-in-parallel)
    - [Reporting Test Coverage](#reporting-test-coverage)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is built with testing in mind. In fact, support for testing with PHPUnit is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications. -->
Laravel은 테스트를 염두에 두고 설계된 프레임워크입니다. 실제로, PHPUnit을 이용한 테스트 지원이 기본으로 내장되어 있으며, 애플리케이션에는 이미 `phpunit.xml` 파일이 준비되어 있습니다. 또한, Laravel은 애플리케이션 테스트를 더 간결하게 작성할 수 있게 도와주는 다양한 헬퍼 메서드도 함께 제공합니다.

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
기본적으로, 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit`이라는 두 개의 하위 디렉터리가 포함되어 있습니다. 유닛 테스트(Unit test)는 코드의 아주 작은, 고립된 부분을 집중적으로 테스트하는 데 사용합니다. 대부분의 유닛 테스트는 한 개의 메서드를 검증하는 데 초점을 맞춥니다. "Unit" 폴더에 있는 테스트들은 Laravel 애플리케이션을 부팅하지 않으므로, 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
피처 테스트(Feature test)는 여러 객체 사이의 상호작용이나 JSON 엔드포인트를 통한 전체 HTTP 요청 등, 코드의 더 넓은 범위를 테스트할 수 있습니다. **일반적으로 테스트의 대부분은 피처 테스트로 작성하는 것이 좋습니다. 이러한 유형의 테스트가 시스템 전체가 의도대로 동작하는지 가장 확실하게 검증할 수 있기 때문입니다.**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/phpunit` or `php artisan test` commands to run your tests. -->
`Feature`와 `Unit` 디렉터리에는 각각 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 돌릴 수 있습니다.

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/9.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver while testing, meaning no session or cache data will be persisted while testing. -->
테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 자동으로 [configuration environment](/docs/9.x/configuration#environment-configuration)을 `testing`으로 지정합니다. 또한 테스트 환경에서는 세션과 캐시도 자동으로 `array` 드라이버로 설정되어, 테스트 중에는 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
필요에 따라 본인만의 테스트 환경 설정 값을 자유롭게 정의할 수도 있습니다. `testing` 환경 변수들은 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있습니다. 단, 테스트를 실행하기 전에 반드시 `config:clear` 아티즌 명령어로 설정 캐시를 삭제하시기 바랍니다!

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
추가적으로, 프로젝트의 루트에 `.env.testing` 파일을 생성할 수도 있습니다. 이 파일은 PHPUnit 테스트를 실행하거나, `--env=testing` 옵션과 함께 아티즌 명령어를 사용할 때 기존의 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
<!-- #### The `CreatesApplication` Trait -->
#### The `CreatesApplication` Trait

<!-- Laravel includes a `CreatesApplication` trait that is applied to your application's base `TestCase` class. This trait contains a `createApplication` method that bootstraps the Laravel application before running your tests. It's important that you leave this trait at its original location as some features, such as Laravel's parallel testing feature, depend on it. -->
Laravel은 애플리케이션의 기본 `TestCase` 클래스에 `CreatesApplication` 트레이트를 포함시킵니다. 이 트레이트는 테스트를 실행하기 전에 Laravel 애플리케이션을 부팅하는 `createApplication` 메서드를 가지고 있습니다. 이 트레이트는 Laravel의 병렬 테스트 기능 등 일부 기능의 동작에 꼭 필요하므로, 원래 위치에 그대로 두어야 합니다.

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
새로운 테스트를 생성하려면, `make:test` 아티즌 명령어를 사용하면 됩니다. 기본적으로 생성되는 테스트 파일은 `tests/Feature` 디렉터리에 저장됩니다.

```shell
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
만약 `tests/Unit` 디렉터리 안에 테스트를 만들고 싶다면, `make:test` 명령어에 `--unit` 옵션을 추가하면 됩니다.

```shell
php artisan make:test UserTest --unit
```

[Pest PHP](https://pestphp.com) 스타일의 테스트를 만들고 싶다면, `--pest` 옵션을 추가하면 됩니다.

<!-- If you would like to create a [Pest PHP](https://pestphp.com) test, you may provide the `--pest` option to the `make:test` command: -->
이 경우에도 `make:test` 명령어에 옵션을 전달합니다.

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!NOTE]
> 테스트 스텁은 [stub publishing](/docs/9.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<!-- Once the test has been generated, you may define test methods as you normally would using [PHPUnit](https://phpunit.de). To run your tests, execute the `vendor/bin/phpunit` or `php artisan test` command from your terminal: -->
테스트 파일이 생성된 후, [PHPUnit](https://phpunit.de)에서 사용하는 것과 동일한 방법으로 테스트 메서드를 작성하면 됩니다. 테스트를 실행하려면 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 사용하세요.

```
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> 테스트 클래스 안에 직접 `setUp` / `tearDown` 메서드를 정의할 경우, 반드시 부모 클래스의 `parent::setUp()` / `parent::tearDown()`도 호출해야 합니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `phpunit`: -->
앞서 설명한 대로, 테스트 코드를 작성한 뒤에는 `phpunit` 명령어로 실행할 수 있습니다.

```shell
./vendor/bin/phpunit
```

<!-- In addition to the `phpunit` command, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`phpunit` 명령어 외에도, 아티즌의 `test` 명령어로도 테스트를 실행할 수 있습니다. 아티즌 테스트 러너는 개발과 디버깅이 쉬워지도록 상세한 테스트 리포트를 제공합니다.

```shell
php artisan test
```

<!-- Any arguments that can be passed to the `phpunit` command may also be passed to the Artisan `test` command: -->
`phpunit`에 전달할 수 있는 모든 인수는 아티즌 `test` 명령어에도 그대로 사용할 수 있습니다.

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests In Parallel -->
### Running Tests In Parallel

<!-- By default, Laravel and PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, ensure your application depends on version `^5.3` or greater of the `nunomaduro/collision` package. Then, include the `--parallel` option when executing the `test` Artisan command: -->
기본적으로 Laravel과 PHPUnit은 테스트를 한 번에 하나의 프로세스에서 순차적으로 실행합니다. 하지만, 여러 개의 프로세스를 동시에 사용해서 테스트를 병렬로 실행하면 테스트 시간을 크게 단축할 수 있습니다. 먼저, 애플리케이션에 `nunomaduro/collision` 패키지 버전 `^5.3` 이상이 설치되어 있어야 합니다. 그 다음, 아티즌 `test` 명령어에 `--parallel` 옵션을 추가해주세요.

```shell
php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
Laravel은 기본적으로 해당 머신의 CPU 코어 수만큼 프로세스를 만들어 병렬 실행을 합니다. 직접 프로세스 개수를 조정하고 싶으면 `--processes` 옵션을 사용하세요.

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 테스트를 병렬로 실행할 때 일부 PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing & Databases -->
#### Parallel Testing & Databases

<!-- As long as you have configured a primary database connection, Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
기본 데이터베이스 연결이 설정되어 있으면, Laravel은 병렬로 실행 중인 각 테스트 프로세스 별로 테스트용 데이터베이스를 자동으로 생성 및 마이그레이션합니다. 이때 각 테스트 데이터베이스 이름에는 프로세스별 고유 토큰이 뒤에 붙습니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있다면, Laravel은 `your_db_test_1`, `your_db_test_2`와 같은 테스트 데이터베이스를 각각 생성해 사용합니다.

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
테스트 데이터베이스는 기본적으로 `test` 아티즌 명령이 다시 호출될 때까지 그대로 유지되어, 이후 `test` 호출에서도 재사용됩니다. 데이터베이스를 매번 새로 만들고 싶다면 `--recreate-databases` 옵션을 추가하세요.

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
가끔, 여러 테스트 프로세스가 안전하게 사용할 수 있도록 애플리케이션 테스트용 리소스를 준비해야 할 수도 있습니다.

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` 파사드를 활용하면, 프로세스 및 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 지정한 클로저는 프로세스 토큰인 `$token`과 현재 테스트 케이스인 `$testCase`를 인자로 받습니다.

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        ParallelTesting::setUpProcess(function ($token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function ($token, $testCase) {
            // ...
        });

        // Executed when a test database is created...
        ParallelTesting::setUpTestDatabase(function ($database, $token) {
            Artisan::call('db:seed');
        });

        ParallelTesting::tearDownTestCase(function ($token, $testCase) {
            // ...
        });

        ParallelTesting::tearDownProcess(function ($token) {
            // ...
        });
    }
}
```

<a name="accessing-the-parallel-testing-token"></a>
<!-- #### Accessing The Parallel Testing Token -->
#### Accessing The Parallel Testing Token

<!-- If you would like to access the current parallel process "token" from any other location in your application's test code, you may use the `token` method. This token is a unique, string identifier for an individual test process and may be used to segment resources across parallel test processes. For example, Laravel automatically appends this token to the end of the test databases created by each parallel testing process: -->
애플리케이션의 테스트 코드 내 다른 위치에서 현재 병렬 프로세스의 "토큰"에 접근하고 싶으면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 각 테스트 프로세스별로 유일한 문자열 식별자이며, 병렬 테스트 환경에서 리소스를 분리·구분하는 데 활용됩니다. 예를 들어, Laravel은 병렬 테스트 데이터베이스 이름 뒤에 이 토큰을 자동으로 붙입니다.

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
<!-- ### Reporting Test Coverage -->
### Reporting Test Coverage

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

<!-- When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command: -->
애플리케이션 테스트를 실행할 때, 테스트 케이스가 실제로 얼마나 애플리케이션 코드를 실행·커버하는지 확인하고 싶을 수 있습니다. 이를 위해, `test` 명령어 실행 시 `--coverage` 옵션을 추가하면 됩니다.

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
<!-- #### Enforcing A Minimum Coverage Threshold -->
#### Enforcing A Minimum Coverage Threshold

<!-- You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met: -->
`--min` 옵션을 이용하면, 애플리케이션 테스트 커버리지의 최소 기준을 지정할 수 있습니다. 설정한 커버리지 기준에 미달하면 테스트가 실패하게 됩니다.

```shell
php artisan test --coverage --min=80.3
```
