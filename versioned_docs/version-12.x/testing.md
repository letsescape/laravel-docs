# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [병렬로 테스트 실행](#running-tests-in-parallel)
    - [테스트 커버리지 리포트](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)
- [설정 캐싱](#configuration-caching)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로 [Pest](https://pestphp.com) 및 [PHPUnit](https://phpunit.de)을 활용한 테스트가 기본적으로 지원되며, `phpunit.xml` 파일도 이미 애플리케이션에 설정되어 있습니다. 프레임워크는 애플리케이션을 효과적으로 테스트할 수 있도록 다양한 헬퍼 메서드도 제공합니다.

기본적으로 애플리케이션의 `tests` 디렉토리에는 `Feature`와 `Unit`이라는 두 개의 하위 디렉토리가 존재합니다. 단위 테스트(Unit test)는 코드의 매우 작은, 분리된 부분에 집중하는 테스트입니다. 대부분의 경우 단위 테스트는 하나의 메서드만을 검증합니다. "Unit" 테스트 디렉토리에 위치한 테스트들은 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션의 데이터베이스나 기타 프레임워크 서비스에 접근할 수 없습니다.

기능 테스트(Feature test)는 여러 오브젝트 간의 상호작용이나, 심지어 전체 HTTP 요청이 JSON 엔드포인트에 도달하는 모습까지 좀 더 큰 코드 범위를 검증할 수 있습니다. **일반적으로 테스트의 대부분은 기능 테스트로 작성하는 것이 좋습니다. 이러한 테스트가 시스템 전체가 의도한 대로 동작하는지 가장 높은 신뢰도로 보장합니다.**

`Feature` 및 `Unit` 테스트 디렉토리 모두에 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는, `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 실행하여 테스트를 수행할 수 있습니다.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때 Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [설정 환경](/docs/12.x/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한 세션과 캐시도 `array` 드라이버로 자동 설정하여, 테스트 실행 중에는 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

필요에 따라 기타 테스트 환경 관련 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 지정할 수 있고, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 지워야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가로, 프로젝트의 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 Artisan 명령어를 사용할 때 `.env` 파일 대신 참조됩니다.

<a name="creating-tests"></a>
## 테스트 생성 (Creating Tests)

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 생성되는 테스트는 `tests/Feature` 디렉토리에 위치합니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉토리 내에 테스트를 생성하고 싶다면, `make:test` 명령어를 실행할 때 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 수정할 수 있습니다.

테스트가 생성되면, Pest 또는 PHPUnit을 이용해 테스트를 작성할 수 있습니다. 테스트 실행은 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어로 수행합니다:

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
> 테스트 클래스 내부에 직접 `setUp` / `tearDown` 메서드를 정의한다면, 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 일반적으로는 `setUp`에서 가장 처음 `parent::setUp()`을, `tearDown`에서 마지막에 `parent::tearDown()`을 호출하는 것이 좋습니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

앞서 설명한 대로, 테스트를 작성한 후에는 `pest` 또는 `phpunit`을 사용해 테스트를 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest`나 `phpunit` 명령 외에도, `test` Artisan 명령어로도 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발과 디버깅을 더 용이하게 해주는 상세한 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 그대로 사용할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬로 테스트 실행 (Running Tests in Parallel)

기본적으로 Laravel과 Pest / PHPUnit은 한 개의 프로세스 안에서 순차적으로 테스트를 실행합니다. 하지만 테스트를 여러 프로세스에서 동시에 실행하면 테스트 소요 시간을 크게 단축할 수 있습니다. 먼저, `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그리고 `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가합니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 현재 머신의 CPU 코어 수 만큼 프로세스를 생성합니다. 필요하다면 `--processes` 옵션으로 프로세스 수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시, 일부 Pest / PHPUnit 옵션(`--do-not-cache-result` 등)은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 구성되어 있다면, Laravel은 테스트를 병렬로 실행하는 각 프로세스마다 자동으로 별도의 테스트 데이터베이스를 생성 및 마이그레이션합니다. 테스트 데이터베이스 이름은 각 프로세스 별로 고유한 토큰이 접미사로 붙으며 구분됩니다. 예를 들어 두 개의 병렬 테스트 프로세스가 있다면, Laravel은 `your_db_test_1`과 `your_db_test_2` 데이터베이스를 생성하여 사용합니다.

기본적으로 테스트 데이터베이스는 여러 번의 `test` Artisan 명령 호출 사이에도 유지되어, 이후 테스트에서도 재사용할 수 있습니다. 하지만, 언제든지 `--recreate-databases` 옵션으로 데이터베이스를 새로 생성할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

가끔은 애플리케이션 테스트에서 사용하는 특정 자원을 여러 테스트 프로세스에서 안전하게 사용할 수 있도록 미리 준비해야 할 경우가 있습니다.

`ParallelTesting` 파사드를 사용하면, 프로세스 또는 테스트 케이스별 `setUp`과 `tearDown`에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 프로세스 토큰을 담은 `$token` 변수와 현재 테스트 케이스를 나타내는 `$testCase` 변수를 인자로 받습니다:

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

        // 테스트 데이터베이스가 생성될 때 실행됩니다...
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

애플리케이션의 테스트 코드 다른 어느 곳에서든, 현재 병렬 프로세스의 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스를 식별하는 고유한 문자열이며, 병렬 테스트 실행 환경에서 자원을 구분 관리하는 데 사용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스에서 생성하는 테스트 데이터베이스 이름 끝에 이 토큰을 자동으로 붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 리포트 (Reporting Test Coverage)

> [!WARNING]
> 이 기능을 사용하려면 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션 테스트를 실행할 때 실제로 테스트 코드가 애플리케이션 코드를 얼마나 커버하고 있는지, 각 테스트가 얼마나 많은 코드를 사용하는지 확인하고 싶을 수 있습니다. 이를 위해, `test` 명령어 실행 시 `--coverage` 옵션을 제공할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 강제

`--min` 옵션을 사용하면 애플리케이션의 최소 테스트 커버리지 기준을 설정할 수 있습니다. 지정한 기준에 미치지 못하면 테스트가 실패합니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 러너는 애플리케이션에서 가장 느린 테스트 목록을 확인할 수 있는 편리한 기능도 제공합니다. `test` 명령어에 `--profile` 옵션을 추가하면, 가장 오래 걸리는 상위 10개의 테스트 목록을 확인할 수 있어, 테스트 속도를 향상시켜야 하는 부분을 쉽게 파악할 수 있습니다:

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

테스트를 실행할 때, Laravel은 개별 테스트 메서드마다 애플리케이션을 부트합니다. 설정 파일이 캐시되어 있지 않다면, 테스트 시작 시마다 모든 설정 파일을 다시 읽어야 하므로 느려질 수 있습니다. 한 번 설정을 만들어 모든 테스트에서 재사용하고 싶다면, `Illuminate\Foundation\Testing\WithCachedConfig` 트레이트를 사용할 수 있습니다:

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
