# 테스트: 시작하기 (Testing: Getting Started)

- [소개](#introduction)
- [환경](#environment)
- [테스트 생성](#creating-tests)
- [테스트 실행](#running-tests)
    - [병렬로 테스트 실행하기](#running-tests-in-parallel)
    - [테스트 커버리지 보고](#reporting-test-coverage)
    - [테스트 프로파일링](#profiling-tests)
- [설정 캐싱](#configuration-caching)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 테스트를 염두에 두고 설계되었습니다. 실제로, [Pest](https://pestphp.com)와 [PHPUnit](https://phpunit.de)에 대한 지원이 기본적으로 포함되어 있으며, 애플리케이션의 루트 디렉터리에 이미 `phpunit.xml` 파일이 설정되어 있습니다. 프레임워크는 애플리케이션 테스트를 더 표현력 있게 작성할 수 있도록 다양한 헬퍼 메서드도 제공합니다.

기본적으로 애플리케이션의 `tests` 디렉터리에는 `Feature`와 `Unit` 두 개의 디렉터리가 있습니다. 단위 테스트(Unit test)는 코드의 아주 작고 독립적인 부분에 집중하는 테스트입니다. 대부분의 단위 테스트는 하나의 메서드만을 검증하는 경우가 많습니다. "Unit" 테스트 디렉터리 내의 테스트들은 Laravel 애플리케이션을 부트하지 않으므로, 애플리케이션 데이터베이스나 프레임워크의 다른 서비스에 접근할 수 없습니다.

기능 테스트(Feature test)는 여러 객체 간의 상호작용이나 JSON 엔드포인트에 대한 전체 HTTP 요청처럼, 더 넓은 범위의 코드를 테스트할 수 있습니다. **일반적으로, 전체 테스트의 대부분은 기능 테스트로 구성하는 것이 좋습니다. 이러한 유형의 테스트가 시스템 전체가 의도한 대로 동작하는지에 대한 신뢰도를 가장 크게 높여줍니다.**

`Feature`와 `Unit` 테스트 디렉터리 모두에 `ExampleTest.php` 파일이 제공됩니다. 새로운 Laravel 애플리케이션을 설치한 후에는, 아래 명령어 중 하나를 실행하여 테스트를 실행할 수 있습니다: `vendor/bin/pest`, `vendor/bin/phpunit`, `php artisan test`.

<a name="environment"></a>
## 환경 (Environment)

테스트를 실행할 때, Laravel은 `phpunit.xml` 파일에 정의된 환경 변수 덕분에 [설정 환경](/docs/master/configuration#environment-configuration)을 자동으로 `testing`으로 설정합니다. 또한, 세션 및 캐시 드라이버도 자동으로 `array`로 설정되어 테스트 중 세션이나 캐시 데이터가 실제로 저장되지 않습니다.

필요에 따라 추가적인 테스트 환경 설정 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 설정할 수 있지만, 테스트를 실행하기 전에 반드시 `config:clear` Artisan 명령어로 설정 캐시를 비워주어야 합니다!

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

추가적으로, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest와 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 Artisan 명령어를 실행할 때, `.env` 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성 (Creating Tests)

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령어를 사용합니다. 기본적으로 테스트는 `tests/Feature` 디렉터리에 생성됩니다:

```shell
php artisan make:test UserTest
```

`tests/Unit` 디렉터리에 테스트를 생성하고자 한다면, `make:test` 명령어 실행 시 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit
```

> [!NOTE]
> 테스트 스텁은 [스텁 커스터마이징](/docs/master/artisan#stub-customization)을 통해 수정할 수 있습니다.

테스트가 생성되었다면, Pest 또는 PHPUnit을 사용하여 평소대로 테스트 내용을 작성하면 됩니다. 테스트는 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, `php artisan test` 명령어로 실행할 수 있습니다:

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
> 테스트 클래스 내에서 `setUp` / `tearDown` 메서드를 직접 정의할 경우, 반드시 상위 클래스의 `parent::setUp()` / `parent::tearDown()` 메서드도 호출해야 합니다. 일반적으로, 직접 작성한 `setUp` 메서드의 시작에서 `parent::setUp()`을, `tearDown` 메서드의 마지막에서 `parent::tearDown()`을 반드시 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

앞서 언급한 것처럼, 테스트를 작성한 후에는 `pest` 또는 `phpunit`으로 실행할 수 있습니다:

```shell tab=Pest
./vendor/bin/pest
```

```shell tab=PHPUnit
./vendor/bin/phpunit
```

`pest`나 `phpunit` 명령어 외에도, Artisan의 `test` 명령어로 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발 및 디버깅을 쉽게 할 수 있도록 더 자세한(Verbose) 테스트 리포트를 제공합니다:

```shell
php artisan test
```

`pest` 또는 `phpunit` 명령어에 전달 가능한 인수는 Artisan `test` 명령어에도 동일하게 사용할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 병렬로 테스트 실행하기 (Running Tests in Parallel)

기본적으로, Laravel과 Pest / PHPUnit은 모든 테스트를 한 프로세스에서 순차적으로 실행합니다. 그러나 여러 프로세스에서 동시에 테스트를 실행하면 테스트 실행 시간을 획기적으로 단축할 수 있습니다. 시작하려면, `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그 후, `test` Artisan 명령어 실행 시 `--parallel` 옵션을 추가하면 됩니다:

```shell
composer require brianium/paratest --dev

php artisan test --parallel
```

기본적으로 Laravel은 컴퓨터의 CPU 코어 개수만큼 프로세스를 생성합니다. 프로세스 수는 `--processes` 옵션으로 직접 지정할 수도 있습니다:

```shell
php artisan test --parallel --processes=4
```

> [!WARNING]
> 병렬 테스트 실행 시, `--do-not-cache-result`와 같은 일부 Pest / PHPUnit 옵션은 사용할 수 없습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결이 설정되어 있다면, Laravel은 각 테스트 프로세스별로 테스트 데이터베이스를 자동으로 생성 및 마이그레이션해줍니다. 테스트 데이터베이스는 프로세스별로 고유한 식별자인 프로세스 토큰이 접미사로 추가되어 생성됩니다. 예를 들어, 병렬 테스트 프로세스가 두 개인 경우, `your_db_test_1`과 `your_db_test_2` 데이터베이스가 생성 및 사용됩니다.

테스트 데이터베이스는 기본적으로 `test` Artisan 명령어를 여러 번 호출해도 계속 사용됩니다. 다시 생성하려면 `--recreate-databases` 옵션을 사용할 수 있습니다:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 Hooks

어떤 경우에는, 애플리케이션 테스트에서 사용하는 특정 리소스를 여러 테스트 프로세스에서 안전하게 사용할 수 있도록 준비해야 할 수 있습니다.

`ParallelTesting` 파사드를 이용하면, 프로세스 또는 테스트 케이스의 `setUp`과 `tearDown` 시점에 실행할 코드를 지정할 수 있습니다. 전달되는 클로저는 프로세스 토큰(`$token`)과 현재 테스트 케이스(`$testCase`)를 매개변수로 받습니다:

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

애플리케이션의 다른 테스트 코드에서 현재 병렬 프로세스의 "토큰"을 사용하고 싶다면, `token` 메서드를 사용할 수 있습니다. 이 토큰은 각 테스트 프로세스를 식별하는 고유한 문자열이며, 병렬 테스트 진행 시 리소스 분할 등 여러 용도로 사용할 수 있습니다. 예를 들어, Laravel은 자동으로 각 병렬 테스트 프로세스가 생성한 테스트 데이터베이스 이름의 끝에 이 토큰을 붙입니다:

```
$token = ParallelTesting::token();
```

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고 (Reporting Test Coverage)

> [!WARNING]
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

애플리케이션의 테스트를 실행할 때, 실제로 테스트 케이스가 얼마나 애플리케이션 코드를 커버하고 있는지, 그리고 테스트 중 어느 정도의 코드가 사용되는지 확인하고 싶을 수 있습니다. 이를 위해 `test` 명령어 실행 시 `--coverage` 옵션을 사용할 수 있습니다:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 임계값 설정

`--min` 옵션을 사용하면 애플리케이션에 대한 최소 테스트 커버리지 임계값을 정의할 수 있습니다. 이 임계값을 충족하지 못하면 테스트는 실패하게 됩니다:

```shell
php artisan test --coverage --min=80.3
```

<a name="profiling-tests"></a>
### 테스트 프로파일링 (Profiling Tests)

Artisan 테스트 러너는 애플리케이션에서 실행된 가장 느린 테스트들을 쉽게 확인할 수 있는 기능도 제공합니다. `test` 명령어에 `--profile` 옵션을 추가하면, 상위 10개의 가장 느린 테스트를 보여주어 테스트 코드의 성능을 개선할 수 있는 부분을 손쉽게 찾아볼 수 있습니다:

```shell
php artisan test --profile
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

테스트를 실행할 때, Laravel은 각 테스트 메서드마다 애플리케이션을 부트합니다. 설정 파일이 캐싱되어 있지 않으면, 테스트가 시작될 때마다 애플리케이션 내 모든 설정 파일을 매번 읽어야 합니다. 한 번만 설정을 빌드하고 해당 실행 내 모든 테스트에서 이를 재사용하려면, `Illuminate\Foundation\Testing\WithCachedConfig` 트레이트를 사용할 수 있습니다:

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
