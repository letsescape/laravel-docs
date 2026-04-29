# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [병렬 테스트 실행](#running-tests-in-parallel)
    - [테스트 커버리지 보고](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)
- [설정 캐싱](#configuration-caching)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 만들어졌습니다. 실제로 [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)을 사용한 테스트 지원이 기본으로 포함되어 있으며, 애플리케이션을 위한 `phpunit.xml` 파일도 이미 설정되어 있습니다. 또한 프레임워크에는 애플리케이션을 표현력 있게 테스트할 수 있는 편리한 헬퍼 메서드가 함께 제공됩니다.

기본적으로 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 디렉터리가 포함되어 있습니다. 단위 테스트는 코드의 매우 작고 격리된 부분에 집중하는 테스트입니다. 실제로 대부분의 단위 테스트는 하나의 메서드에 집중하는 경우가 많습니다. "Unit" 테스트 디렉터리 안의 테스트는 Laravel 애플리케이션을 부팅하지 않으므로 애플리케이션의 데이터베이스나 다른 프레임워크 서비스에 접근할 수 없습니다.

기능 테스트는 여러 객체가 서로 상호작용하는 방식이나 JSON 엔드포인트로 보내는 전체 HTTP 요청까지 포함하여 코드의 더 큰 부분을 테스트할 수 있습니다. **일반적으로 대부분의 테스트는 기능 테스트여야 합니다. 이런 유형의 테스트는 시스템 전체가 의도한 대로 동작하고 있다는 가장 큰 확신을 제공합니다.**

`Feature`와 `Unit` 테스트 디렉터리에는 모두 `ExampleTest.php` 파일이 제공됩니다. 새 Laravel 애플리케이션을 설치한 후에는 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행하여 테스트를 실행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 때문에 [설정 환경](/docs/13.x/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 Laravel은 세션과 캐시를 자동으로 `array` 드라이버로 설정하여 테스트 중에는 세션이나 캐시 데이터가 유지되지 않도록 합니다.

필요하다면 다른 테스트 환경 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 지워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로 프로젝트 루트에 `.env.testing` 파일을 만들 수 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션으로 Artisan 명령어를 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성 (Creating Tests)

새 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 테스트는 `tests/Feature` 디렉터리에 배치됩니다.

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리 안에 테스트를 생성하고 싶다면 `make:test` 명령어를 실행할 때 `--unit` 옵션을 사용할 수 있습니다.

```shell
php artisan make:test UserTest --unit
```

Laravel의 테스트 기능에 대부분 의존하는 테스트 클래스가 있지만, 특정 테스트 메서드에서는 프레임워크를 부팅할 필요가 없다면 해당 메서드에 `#[UnitTest]` 속성을 적용하여 그 테스트에서만 애플리케이션 부팅을 건너뛸 수 있습니다.

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\Attributes\UnitTest;
use Tests\TestCase;

class LocationServiceTest extends TestCase
{
    public function test_get_coordinates_resolves_address(): void
    {
        // This test uses Laravel's testing features...
    }

    #[UnitTest]
    public function test_get_state_returns_state_from_abbreviation(): void
    {
        // This test runs without booting the application...
    }
}
```

> [!NOTE]
> 테스트 스텁은 [스텁 게시](/docs/13.x/artisan#stub-customization)를 사용하여 사용자 정의할 수 있습니다.

테스트가 생성되면 평소처럼 Pest 또는 PHPUnit을 사용하여 테스트를 정의할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령어를 실행합니다.

```php tab=Pest
<?php

test('basic', function () {
    expect(true)->toBeTrue();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}
```

> [!WARNING]
> 테스트 클래스 안에서 직접 `setUp` / `tearDown` 메서드를 정의하는 경우, 부모 클래스의 해당 `parent::setUp()` / `parent::tearDown()` 메서드를 반드시 호출해야 합니다. 일반적으로 직접 작성한 `setUp` 메서드의 시작 부분에서 `parent::setUp()`을 호출하고, `tearDown` 메서드의 끝부분에서 `parent::tearDown()`을 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

앞서 언급했듯이 테스트를 작성한 후에는 `pest` 또는 `phpunit`을 사용하여 실행할 수 있습니다.

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest` 또는 `phpunit` 명령어 외에도 `test` Artisan 명령어를 사용하여 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발과 디버깅을 더 쉽게 할 수 있도록 자세한 테스트 보고서를 제공합니다.

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 전달할 수 있습니다.

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬 테스트 실행

기본적으로 Laravel과 Pest / PHPUnit은 테스트를 단일 프로세스 안에서 순차적으로 실행합니다. 하지만 여러 프로세스에서 동시에 테스트를 실행하면 테스트 실행 시간을 크게 줄일 수 있습니다. 시작하려면 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그런 다음 `test` Artisan 명령어를 실행할 때 `--parallel` 옵션을 포함합니다.

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 사용 중인 머신에서 사용할 수 있는 CPU 코어 수만큼 프로세스를 생성합니다. 하지만 `--processes` 옵션을 사용하여 프로세스 수를 조정할 수 있습니다.

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 테스트를 병렬로 실행할 때는 일부 Pest / PHPUnit 옵션(예: `--do-not-cache-result`)을 사용할 수 없을 수 있습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결을 설정해 두었다면, Laravel은 테스트를 실행하는 각 병렬 프로세스마다 테스트 데이터베이스를 생성하고 마이그레이션하는 작업을 자동으로 처리합니다. 테스트 데이터베이스에는 프로세스마다 고유한 프로세스 토큰이 접미사로 붙습니다. 예를 들어 병렬 테스트 프로세스가 두 개라면 Laravel은 `your_db_test_1`과 `your_db_test_2` 테스트 데이터베이스를 생성하고 사용합니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령어 호출 사이에도 유지되므로 이후 `test` 실행에서 다시 사용할 수 있습니다. 하지만 `--recreate-databases` 옵션을 사용하면 테스트 데이터베이스를 다시 생성할 수 있습니다.

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

때로는 여러 테스트 프로세스가 안전하게 사용할 수 있도록 애플리케이션 테스트에서 사용하는 특정 리소스를 준비해야 할 수 있습니다.

`ParallelTesting` 파사드를 사용하면 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달된 클로저는 각각 프로세스 토큰과 현재 테스트 케이스를 담고 있는 `$token` 및 `$testCase` 변수를 받습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;
use PHPUnit\Framework\TestCase;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        ParallelTesting::setUpProcess(function (int $token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        // Executed when a test database is created...
        ParallelTesting::setUpTestDatabase(function (string $database, int $token) {
            Artisan::call('db:seed');
        });

        ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        ParallelTesting::tearDownProcess(function (int $token) {
            // ...
        });
    }
}
```

<a name="accessing-the-parallel-testing-token"></a>
#### 병렬 테스트 토큰 접근

애플리케이션 테스트 코드의 다른 위치에서 현재 병렬 프로세스 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 위한 고유한 문자열 식별자이며, 병렬 테스트 프로세스 간에 리소스를 분리하는 데 사용할 수 있습니다. 예를 들어 Laravel은 각 병렬 테스트 프로세스가 생성한 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 추가합니다.

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때 테스트 케이스가 실제로 애플리케이션 코드를 커버하고 있는지, 그리고 테스트 실행 중 애플리케이션 코드가 얼마나 사용되는지 확인하고 싶을 수 있습니다. 이를 수행하려면 `test` 명령어를 호출할 때 `--coverage` 옵션을 제공하면 됩니다.

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 임계값 강제

`--min` 옵션을 사용하여 애플리케이션의 최소 테스트 커버리지 임계값을 정의할 수 있습니다. 이 임계값을 충족하지 못하면 테스트 스위트가 실패합니다.

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링

Artisan 테스트 러너에는 애플리케이션에서 가장 느린 테스트를 나열하는 편리한 기능도 포함되어 있습니다. `--profile` 옵션과 함께 `test` 명령어를 호출하면 가장 느린 테스트 10개의 목록이 표시되므로, 테스트 스위트의 실행 속도를 높이기 위해 어떤 테스트를 개선할 수 있는지 쉽게 조사할 수 있습니다.

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

테스트를 실행할 때 Laravel은 각각의 개별 테스트 메서드마다 애플리케이션을 부팅합니다. 캐시된 설정 파일이 없으면 테스트 시작 시 애플리케이션의 각 설정 파일을 로드해야 합니다. 설정을 한 번 빌드한 뒤 단일 실행의 모든 테스트에서 재사용하려면 `Illuminate\Foundation\Testing\WithCachedConfig` trait을 사용할 수 있습니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithCachedConfig;

pest()->use(WithCachedConfig::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithCachedConfig;
use Tests\TestCase;

class ConfigTest extends TestCase
{
    use WithCachedConfig;

    // ...
}
```
