<!-- # Testing: Getting Started -->
# Testing: Getting Started

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
    - [Running Tests In Parallel](#running-tests-in-parallel)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is built with testing in mind. In fact, support for testing with PHPUnit is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications. -->
Laravel은 처음부터 테스트를 염두에 두고 설계되었습니다. 실제로, PHPUnit을 활용한 테스트 지원이 기본적으로 포함되어 있으며, 애플리케이션에는 이미 설정이 완료된 `phpunit.xml` 파일이 제공됩니다. 또한, 프레임워크는 애플리케이션 테스트를 더 간편하고 명확하게 작성할 수 있도록 다양한 헬퍼 메서드도 함께 제공합니다.

<!-- By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Tests within your "Unit" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services. -->
기본적으로 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 하위 디렉터리가 있습니다. 유닛 테스트(Unit test)는 코드 내 아주 작은, 독립적인 부분만을 집중적으로 테스트합니다. 실제로 대부분의 유닛 테스트는 하나의 메서드만을 다루는 경우가 많습니다. "Unit" 테스트 디렉터리 내의 테스트는 Laravel 애플리케이션을 부팅하지 않으므로, 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

<!-- Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint. **Generally, most of your tests should be feature tests. These types of tests provide the most confidence that your system as a whole is functioning as intended.** -->
기능 테스트(Feature test)는 여러 객체 간의 상호작용이나, JSON 엔드포인트에 대한 전체 HTTP 요청 등 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트로 작성하는 것이 좋습니다. 이런 유형의 테스트가 시스템 전체가 의도한 대로 동작하는지 가장 높은 신뢰를 제공합니다.**

<!-- An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, execute the `vendor/bin/phpunit` or `php artisan test` commands to run your tests. -->
각 테스트 디렉터리(`Feature`, `Unit`) 모두에 `ExampleTest.php` 파일이 기본 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
<!-- ## Environment -->
## Environment

<!-- When running tests, Laravel will automatically set the [configuration environment](/docs/8.x/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver while testing, meaning no session or cache data will be persisted while testing. -->
테스트 실행 시 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [configuration environment](/docs/8.x/configuration#environment-configuration)을 자동으로 `testing`으로 변경합니다. 또한, 테스트 중에는 세션과 캐시 드라이버가 자동으로 `array`로 설정되어, 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

<!-- You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests! -->
필요하다면 추가적인 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경용 변수들은 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트 실행 전에는 반드시 `config:clear` 아티즌 명령어로 설정 캐시를 삭제해야 합니다.

<a name="the-env-testing-environment-file"></a>
<!-- #### The `.env.testing` Environment File -->
#### The `.env.testing` Environment File

<!-- In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running PHPUnit tests or executing Artisan commands with the `--env=testing` option. -->
추가로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수도 있습니다. 이 파일은 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션을 사용하는 아티즌 명령어 실행 시 `.env` 파일 대신 사용됩니다.

<a name="the-creates-application-trait"></a>
<!-- #### The `CreatesApplication` Trait -->
#### The `CreatesApplication` Trait

<!-- Laravel includes a `CreatesApplication` trait that is applied to your application's base `TestCase` class. This trait contains a `createApplication` method that bootstraps the Laravel application before running your tests. It's important that you leave this trait at its original location as some features, such as Laravel's parallel testing feature, depend on it. -->
Laravel은 애플리케이션의 기본 `TestCase` 클래스에 `CreatesApplication` 트레이트(trait)를 포함합니다. 이 트레이트에는 테스트 실행 전에 Laravel 애플리케이션을 부트스트랩하는 `createApplication` 메서드가 담겨 있습니다. 이 트레이트는 해당 위치에 그대로 두어야 하며, Laravel의 병렬 테스트 등 일부 기능이 이를 필요로 합니다.

<a name="creating-tests"></a>
<!-- ## Creating Tests -->
## Creating Tests

<!-- To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory: -->
새로운 테스트 케이스를 생성하려면 `make:test` 아티즌 명령어를 사용합니다. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

```
php artisan make:test UserTest
```

<!-- If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command: -->
만약 `tests/Unit` 디렉터리 내에 테스트를 생성하고 싶다면, `make:test` 명령어 실행 시 `--unit` 옵션을 추가하면 됩니다:

```
php artisan make:test UserTest --unit
```

<!-- If you would like to create a [Pest PHP](https://pestphp.com) test, you may provide the `--pest` option to the `make:test` command: -->
[Pest PHP](https://pestphp.com) 방식의 테스트를 생성하고자 한다면, `make:test` 명령어에 `--pest` 옵션을 사용할 수 있습니다:

```
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> [!TIP]
> 테스트 스텁(stub)은 [stub publishing](/docs/8.x/artisan#stub-customization)를 활용해 직접 커스터마이즈할 수 있습니다.

<!-- Once the test has been generated, you may define test methods as you normally would using [PHPUnit](https://phpunit.de). To run your tests, execute the `vendor/bin/phpunit` or `php artisan test` command from your terminal: -->
테스트가 생성되면, [PHPUnit](https://phpunit.de)을 사용하듯이 원하는 대로 테스트 메서드를 정의하면 됩니다. 테스트를 실행하려면, 터미널에서 `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 입력합니다:

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

> [!NOTE]
> 테스트 클래스에 직접 `setUp` 또는 `tearDown` 메서드를 정의하는 경우, 반드시 부모 클래스의 `parent::setUp()` 또는 `parent::tearDown()` 메서드를 호출해야 합니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- As mentioned previously, once you've written tests, you may run them using `phpunit`: -->
앞서 언급한 대로, 작성한 테스트는 `phpunit` 명령어로 실행할 수 있습니다:


<!--     ./vendor/bin/phpunit -->
    ./vendor/bin/phpunit


<!-- In addition to the `phpunit` command, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging: -->
`phpunit` 명령어 외에도 아티즌의 `test` 명령어를 이용해 테스트를 실행할 수 있습니다. 아티즌 테스트 러너는 개발 및 디버깅에 도움이 되도록 상세한 테스트 리포트를 제공합니다:

```
php artisan test
```

<!-- Any arguments that can be passed to the `phpunit` command may also be passed to the Artisan `test` command: -->
`phpunit` 명령어에 전달할 수 있는 모든 인수는 아티즌 `test` 명령어에도 그대로 사용할 수 있습니다:

```
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
<!-- ### Running Tests In Parallel -->
### Running Tests In Parallel

<!-- By default, Laravel and PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, ensure your application depends on version `^5.3` or greater of the `nunomaduro/collision` package. Then, include the `--parallel` option when executing the `test` Artisan command: -->
기본적으로 Laravel과 PHPUnit은 단일 프로세스에서 차례대로(순차적으로) 테스트를 실행합니다. 하지만 여러 프로세스를 병렬로 활용하면 전체 테스트 소요 시간을 크게 줄일 수 있습니다. 이를 시작하려면 애플리케이션에 `nunomaduro/collision` 패키지의 버전 `^5.3` 이상이 필요합니다. 그 후, 아티즌 `test` 명령어에 `--parallel` 옵션을 추가하면 됩니다:

```
php artisan test --parallel
```

<!-- By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option: -->
Laravel은 기본적으로 시스템의 CPU 코어 수만큼의 프로세스를 생성하여 테스트를 병렬 수행합니다. 직접 프로세스 개수를 지정하고 싶다면 `--processes` 옵션을 사용하면 됩니다:

```
php artisan test --parallel --processes=4
```

> [!NOTE]
> 테스트를 병렬로 실행하는 경우, 일부 PHPUnit 옵션(예: `--do-not-cache-result`)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
<!-- #### Parallel Testing & Databases -->
#### Parallel Testing & Databases

<!-- Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases. -->
Laravel은 각 병렬 프로세스마다 테스트 데이터베이스를 자동으로 생성 및 마이그레이션합니다. 테스트 데이터베이스는 각 프로세스별로 고유한 토큰이 뒤에 붙어 생성됩니다. 예를 들어, 병렬 테스트 프로세스가 두 개라면 `your_db_test_1`, `your_db_test_2`와 같은 데이터베이스가 만들어집니다.

<!-- By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option: -->
기본적으로 테스트 데이터베이스는 `test` 아티즌 명령어 실행 간에 유지되어, 이후 `test` 실행 시에도 재사용할 수 있습니다. 하지만, 데이터베이스를 새로 생성하고 싶다면 `--recreate-databases` 옵션을 사용할 수 있습니다:

```
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
<!-- #### Parallel Testing Hooks -->
#### Parallel Testing Hooks

<!-- Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes. -->
애플리케이션 테스트에서 여러 프로세스가 동시에 안전하게 사용할 수 있도록 특정 리소스를 미리 준비해야 할 때가 있습니다.

<!-- Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively: -->
`ParallelTesting` 파사드(facade)를 사용하면, 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 각 클로저에는 프로세스 토큰(`$token`)과 현재 테스트 케이스(`$testCase`)가 전달됩니다:

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

<!-- If you would like to access to current parallel process "token" from any other location in your application's test code, you may use the `token` method. This token is a unique, string identifier for an individual test process and may be used to segment resources across parallel test processes. For example, Laravel automatically appends this token to the end of the test databases created by each parallel testing process: -->
애플리케이션 테스트 코드 어디에서든 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 각각의 테스트 프로세스를 고유하게 식별하는 문자열로, 병렬 테스트 과정에서 리소스를 분리해서 사용할 때 활용할 수 있습니다. 예를 들어 Laravel은 각 병렬 테스트 프로세스마다 생성하는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

```
$token = ParallelTesting::token();
```
