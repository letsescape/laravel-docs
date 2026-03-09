# Laravel Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 재설정](#resetting-the-database-after-each-test)
    - [테스트 실행 중](#running-tests)
    - [환경 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 만들기](#creating-browsers)
    - [내비게이션](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행 중](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력을 디스크에 저장](#storing-console-output-to-disk)
    - [페이지 소스를 디스크에 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [Dusk 선택기](#dusk-selectors)
    - [텍스트, 값 및 속성](#text-values-and-attributes)
    - [양식 상호 작용](#interacting-with-forms)
    - [파일첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용하기](#using-the-keyboard)
    - [마우스 사용하기](#using-the-mouse)
    - [JavaScript 대화상자](#javascript-dialogs)
    - [인라인 프레임과 상호 작용](#interacting-with-iframes)
    - [범위 선택기](#scoping-selectors)
    - [요소를 기다리는 중](#waiting-for-elements)
    - [요소를 뷰로 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성 중](#generating-pages)
    - [페이지 구성](#configuring-pages)
    - [페이지 탐색](#navigating-to-pages)
    - [단축 선택기](#shorthand-selectors)
    - [페이지 방법](#page-methods)
- [구성품](#components)
    - [구성요소 생성](#generating-components)
    - [컴포넌트 사용하기](#using-components)
- [지속적 통합](#continuous-integration)
    - [헤로쿠 CI](#running-tests-on-heroku-ci)
    - [트래비스 CI](#running-tests-on-travis-ci)
    - [GitHub 작업](#running-tests-on-github-actions)
    - [치퍼 CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> [Pest 4](https://pestphp.com/)에는 이제 Laravel Dusk에 비해 상당한 성능 및 유용성 향상을 제공하는 자동화된 브라우저 테스트가 포함되어 있습니다. 새로운 프로젝트의 경우 브라우저 테스트를 위해 Pest를 사용하는 것이 좋습니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 풍부하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk에서는 로컬 컴퓨터에 JDK 또는 Selenium을 설치할 필요가 없습니다. 대신, Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 그러나 원하는 다른 Selenium 호환 드라이버를 자유롭게 활용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 종속성을 추가해야 합니다.

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우 프로덕션 환경에 해당 서비스를 **절대** 등록해서는 안 됩니다. 그렇게 하면 임의의 사용자가 귀하의 애플리케이션을 인증할 수 있게 될 수 있습니다.

Dusk 패키지를 설치한 후 `dusk:install` Artisan 명령을 실행합니다. `dusk:install` 명령은 Dusk 테스트의 예인 `tests/Browser` 디렉터리를 생성하고 운영 체제에 맞는 Chrome 드라이버 바이너리를 설치합니다.

```shell
php artisan dusk:install
```

그런 다음 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정합니다. 이 값은 브라우저에서 애플리케이션에 액세스하는 데 사용하는 URL와 일치해야 합니다.

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)을 사용하여 로컬 개발 환경을 관리하는 경우 [Dusk 테스트 구성 및 실행](/docs/12.x/sail#laravel-dusk)에 대한 Sail 설명서도 참조하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

`dusk:install` 명령을 통해 Laravel Dusk에서 설치한 것과 다른 버전의 ChromeDriver를 설치하려면 `dusk:chrome-driver` 명령을 사용할 수 있습니다.

```shell
# Install the latest version of ChromeDriver for your OS...
php artisan dusk:chrome-driver

# Install a given version of ChromeDriver for your OS...
php artisan dusk:chrome-driver 86

# Install a given version of ChromeDriver for all supported OSs...
php artisan dusk:chrome-driver --all

# Install the version of ChromeDriver that matches the detected version of Chrome / Chromium for your OS...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk를 실행하려면 `chromedriver` 바이너리가 필요합니다. Dusk를 실행하는 데 문제가 있는 경우 `chmod -R 0755 vendor/laravel/dusk/bin/` 명령을 사용하여 바이너리가 실행 가능한지 확인해야 합니다.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용하여 브라우저 테스트를 실행합니다. 그러나 자체 Selenium 서버를 시작하고 원하는 브라우저에 대해 테스트를 실행할 수 있습니다.

시작하려면 애플리케이션의 기본 Dusk 테스트 사례인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일 내에서 `startChromeDriver` 메서드에 대한 호출을 제거할 수 있습니다. 이렇게 하면 Dusk가 ChromeDriver를 자동으로 시작하는 것이 중지됩니다.

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

다음으로, `driver` 방법을 수정하여 원하는 URL 및 포트에 연결할 수 있습니다. 또한 WebDriver에 전달되어야 하는 "원하는 기능"을 수정할 수 있습니다.

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
    );
}
```

<a name="getting-started"></a>
## 시작하기 (Getting Started)

<a name="generating-tests"></a>
### 테스트 생성

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령을 사용하십시오. 생성된 테스트는 `tests/Browser` 디렉터리에 배치됩니다.

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 재설정

여러분이 작성하는 대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 검색하는 페이지와 상호 작용합니다. 그러나 Dusk 테스트에서는 `RefreshDatabase` 특성을 절대 사용해서는 안 됩니다. `RefreshDatabase` 특성은 HTTP 요청에 적용할 수 없거나 사용할 수 없는 데이터베이스 트랜잭션을 활용합니다. 대신 `DatabaseMigrations` 특성과 `DatabaseTruncation` 특성이라는 두 가지 옵션이 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 특성은 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 그러나 각 테스트에 대해 데이터베이스 테이블을 삭제하고 다시 만드는 것은 일반적으로 테이블을 자르는 것보다 느립니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    //
}
```

> [!WARNING]
> SQLite 인 메모리 데이터베이스는 Dusk 테스트를 실행할 때 사용되지 않을 수 있습니다. 브라우저는 자체 프로세스 내에서 실행되므로 다른 프로세스의 메모리 내 데이터베이스에 액세스할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 잘림 사용

`DatabaseTruncation` 특성은 데이터베이스 테이블이 올바르게 생성되었는지 확인하기 위해 첫 번째 테스트에서 데이터베이스를 마이그레이션합니다. 그러나 후속 테스트에서는 데이터베이스 테이블이 잘려서 모든 데이터베이스 마이그레이션을 다시 실행하는 것보다 속도가 향상됩니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;

pest()->use(DatabaseTruncation::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;

    //
}
```

기본적으로 이 특성은 `migrations` 테이블을 제외한 모든 테이블을 자릅니다. 잘라야 하는 테이블을 사용자 지정하려면 테스트 클래스에 `$tablesToTruncate` 속성을 정의할 수 있습니다.

> [!NOTE]
> Pest를 사용하는 경우 기본 `DuskTestCase` 클래스 또는 테스트 파일이 확장하는 모든 클래스에서 속성이나 메서드를 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는 테스트 클래스에 `$exceptTables` 속성을 정의하여 잘림에서 제외해야 하는 테이블을 지정할 수 있습니다.

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

테이블을 잘라야 하는 데이터베이스 연결을 지정하려면 테스트 클래스에 `$connectionsToTruncate` 속성을 정의하면 됩니다.

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

데이터베이스 잘림이 수행되기 전이나 후에 코드를 실행하려면 테스트 클래스에 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의하면 됩니다.

```php
/**
 * Perform any work that should take place before the database has started truncating.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * Perform any work that should take place after the database has finished truncating.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행

브라우저 테스트를 실행하려면 `dusk` Artisan 명령을 실행하세요.

```shell
php artisan dusk
```

마지막으로 `dusk` 명령을 실행했을 때 테스트가 실패했다면 먼저 `dusk:fails` 명령을 사용하여 실패한 테스트를 다시 실행하여 시간을 절약할 수 있습니다.

```shell
php artisan dusk:fails
```

`dusk` 명령은 주어진 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)에 대해서만 테스트를 실행할 수 있도록 허용하는 것과 같이 Pest / PHPUnit 테스트 실행기에서 일반적으로 허용되는 모든 인수를 허용합니다.

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)을 사용하여 로컬 개발 환경을 관리하는 경우 [Dusk 테스트 구성 및 실행](/docs/12.x/sail#laravel-dusk)에 대한 Sail 설명서를 참조하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작

기본적으로 Dusk는 자동으로 ChromeDriver 시작을 시도합니다. 특정 시스템에서 이것이 작동하지 않으면 `dusk` 명령을 실행하기 전에 ChromeDriver를 수동으로 시작할 수 있습니다. ChromeDriver를 수동으로 시작하려면 `tests/DuskTestCase.php` 파일의 다음 줄을 주석 처리해야 합니다.

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

또한 9515가 아닌 포트에서 ChromeDriver를 시작하는 경우 올바른 포트를 반영하도록 동일한 클래스의 `driver` 메서드를 수정해야 합니다.

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
### 환경관리

테스트를 실행할 때 Dusk가 자체 환경 파일을 사용하도록 하려면 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만듭니다. 예를 들어, `local` 환경에서 `dusk` 명령을 시작하는 경우 `.env.dusk.local` 파일을 생성해야 합니다.

테스트를 실행할 때 Dusk는 `.env` 파일을 백업하고 Dusk 환경의 이름을 `.env`로 바꿉니다. 테스트가 완료되면 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 사항 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 만들기

시작하려면 애플리케이션에 로그인할 수 있는지 확인하는 테스트를 작성해 보겠습니다. 테스트를 생성한 후 로그인 페이지로 이동하여 자격 증명을 입력하고 "로그인" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 내에서 `browse` 메서드를 호출하면 됩니다.

```php tab=Pest
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $user = User::factory()->create([
        'email' => 'taylor@laravel.com',
    ]);

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/login')
            ->type('email', $user->email)
            ->type('password', 'password')
            ->press('Login')
            ->assertPathIs('/home');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * A basic browser test example.
     */
    public function test_basic_example(): void
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function (Browser $browser) use ($user) {
            $browser->visit('/login')
                ->type('email', $user->email)
                ->type('password', 'password')
                ->press('Login')
                ->assertPathIs('/home');
        });
    }
}
```

위의 예에서 볼 수 있듯이 `browse` 메서드는 클로저를 허용합니다. 브라우저 인스턴스는 Dusk에 의해 이 클로저에 자동으로 전달되며 애플리케이션과 상호 작용하고 애플리케이션에 대해 어설션을 만드는 데 사용되는 주요 개체입니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 만들기

때로는 테스트를 제대로 수행하기 위해 여러 브라우저가 필요할 수도 있습니다. 예를 들어 웹 소켓과 상호 작용하는 채팅 화면을 테스트하려면 여러 브라우저가 필요할 수 있습니다. 여러 브라우저를 생성하려면 `browse` 메소드에 제공된 클로저 서명에 더 많은 브라우저 인수를 추가하기만 하면 됩니다.

```php
$this->browse(function (Browser $first, Browser $second) {
    $first->loginAs(User::find(1))
        ->visit('/home')
        ->waitForText('Message');

    $second->loginAs(User::find(2))
        ->visit('/home')
        ->waitForText('Message')
        ->type('message', 'Hey Taylor')
        ->press('Send');

    $first->waitForText('Hey Taylor')
        ->assertSee('Jeffrey Way');
});
```

<a name="navigation"></a>
### 항해

`visit` 메소드는 애플리케이션 내에서 지정된 URI로 이동하는 데 사용될 수 있습니다.

```php
$browser->visit('/login');
```

`visitRoute` 방법을 사용하여 [라우트라는 이름](/docs/12.x/routing#named-routes)으로 이동할 수 있습니다.

```php
$browser->visitRoute($routeName, $parameters);
```

`back` 및 `forward` 메소드를 사용하여 "뒤로" 및 "앞으로" 탐색할 수 있습니다.

```php
$browser->back();

$browser->forward();
```

`refresh` 메소드를 사용하여 페이지를 새로 고칠 수 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메소드를 사용하여 브라우저 창의 크기를 조정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메소드를 사용하여 브라우저 창을 최대화할 수 있습니다.

```php
$browser->maximize();
```

`fitContent` 메소드는 내용의 크기에 맞게 브라우저 창의 크기를 조정합니다.

```php
$browser->fitContent();
```

테스트가 실패하면 Dusk는 스크린샷을 찍기 전에 콘텐츠에 맞게 브라우저 크기를 자동으로 조정합니다. 테스트 내에서 `disableFitOnFailure` 메소드를 호출하여 이 기능을 비활성화할 수 있습니다.

```php
$browser->disableFitOnFailure();
```

`move` 메소드를 사용하여 브라우저 창을 화면의 다른 위치로 이동할 수 있습니다.

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로

다양한 테스트에서 재사용할 수 있는 사용자 지정 브라우저 메서드를 정의하려면 `Browser` 클래스에서 `macro` 메서드를 사용할 수 있습니다. 일반적으로 [프로바이더 서비스](/docs/12.x/providers) `boot` 메서드에서 이 메서드를 호출해야 합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Browser::macro('scrollToElement', function (string $element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

`macro` 함수는 이름을 첫 번째 인수로 받아들이고 클로저를 두 번째 인수로 받아들입니다. 매크로의 클로저는 `Browser` 인스턴스의 메서드로 매크로를 호출할 때 실행됩니다.

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 입증

인증이 필요한 페이지를 테스트하는 경우가 많습니다. 모든 테스트에 애플리케이션의 로그인 화면과의 상호 작용을 피하기 위해 Dusk의 `loginAs` 메서드를 사용할 수 있습니다. `loginAs` 메서드는 인증 가능한 모델 또는 인증 가능한 모델 인스턴스와 연결된 기본 키를 허용합니다.

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 방법을 사용한 후에는 파일 내의 모든 테스트에 대해 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메소드를 사용하여 암호화된 쿠키의 값을 얻거나 설정할 수 있습니다. 기본적으로 Laravel에서 생성된 모든 쿠키는 암호화됩니다.

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키의 값을 가져오거나 설정하려면 `plainCookie` 메소드를 사용할 수 있습니다.

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` 메소드를 사용하여 주어진 쿠키를 삭제할 수 있습니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행 중

`script` 메소드를 사용하여 브라우저 내에서 임의의 JavaScript 문을 실행할 수 있습니다.

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot` 방법을 사용하여 스크린샷을 찍고 지정된 파일 이름으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다.

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 다양한 중단점에서 일련의 스크린샷을 찍는 데 사용될 수 있습니다.

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메소드는 페이지의 특정 요소에 대한 스크린샷을 찍는 데 사용될 수 있습니다.

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력을 디스크에 저장

`storeConsoleLog` 메소드를 사용하여 현재 브라우저의 콘솔 출력을 주어진 파일 이름으로 디스크에 쓸 수 있습니다. 콘솔 출력은 `tests/Browser/console` 디렉터리에 저장됩니다.

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스를 디스크에 저장

`storeSource` 메소드를 사용하여 현재 페이지의 소스를 주어진 파일 이름으로 디스크에 쓸 수 있습니다. 페이지 소스는 `tests/Browser/source` 디렉터리에 저장됩니다.

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호 작용 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 선택기

요소와 상호 작용하기 위해 좋은 CSS 선택기를 선택하는 것은 Dusk 테스트 작성에서 가장 어려운 부분 중 하나입니다. 시간이 지남에 따라 프론트엔드 변경으로 인해 다음과 같은 CSS 선택기가 테스트를 중단시킬 수 있습니다.

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 선택기를 사용하면 CSS 선택기를 기억하는 대신 효과적인 테스트 작성에 집중할 수 있습니다. 선택기를 정의하려면 HTML 요소에 `dusk` 속성을 추가하세요. 그런 다음 Dusk 브라우저와 상호 작용할 때 선택기 앞에 `@`를 붙여 테스트 내에서 연결된 요소를 조작합니다.

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원하는 경우 `selectorHtmlAttribute` 메소드를 통해 Dusk 선택기가 활용하는 HTML 속성을 사용자 지정할 수 있습니다. 일반적으로 이 메소드는 애플리케이션 `AppServiceProvider`의 `boot` 메소드에서 호출되어야 합니다.

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값 및 속성

<a name="retrieving-setting-values"></a>
#### 값 검색 및 설정

Dusk는 페이지에 있는 요소의 현재 값, 표시 텍스트 및 속성과 상호 작용하기 위한 여러 가지 방법을 제공합니다. 예를 들어, 주어진 CSS 또는 Dusk 선택기와 일치하는 요소의 "값"을 얻으려면 `value` 메소드를 사용하십시오.

```php
// Retrieve the value...
$value = $browser->value('selector');

// Set the value...
$browser->value('selector', 'value');
```

`inputValue` 메소드를 사용하여 주어진 필드 이름을 가진 입력 요소의 "값"을 얻을 수 있습니다.

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 검색

`text` 메소드는 주어진 선택기와 일치하는 요소의 표시 텍스트를 검색하는 데 사용될 수 있습니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 검색

마지막으로 `attribute` 메소드는 주어진 선택자와 일치하는 요소의 속성 값을 검색하는 데 사용될 수 있습니다.

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 양식과 상호 작용

<a name="typing-values"></a>
#### 값 입력

Dusk는 양식 및 입력 요소와 상호 작용하기 위한 다양한 방법을 제공합니다. 먼저 입력 필드에 텍스트를 입력하는 예를 살펴보겠습니다.

```php
$browser->type('email', 'taylor@laravel.com');
```

메서드는 필요한 경우 하나를 허용하지만 CSS 선택기를 `type` 메서드에 전달할 필요는 없습니다. CSS 선택기가 제공되지 않으면 Dusk는 지정된 `name` 속성을 사용하여 `input` 또는 `textarea` 필드를 검색합니다.

내용을 지우지 않고 필드에 텍스트를 추가하려면 `append` 메소드를 사용할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

`clear` 메소드를 사용하여 입력 값을 지울 수 있습니다.

```php
$browser->clear('email');
```

`typeSlowly` 메서드를 사용하면 Dusk에게 천천히 입력하도록 지시할 수 있습니다. 기본적으로 Dusk는 키를 누르는 사이에 100밀리초 동안 일시 중지됩니다. 키 누르기 사이의 시간을 사용자 지정하려면 적절한 수의 밀리초를 메소드의 세 번째 인수로 전달할 수 있습니다.

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드를 사용하여 텍스트를 천천히 추가할 수 있습니다.

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 요소에서 사용 가능한 값을 선택하려면 `select` 방법을 사용할 수 있습니다. `type` 방법과 마찬가지로 `select` 방법에는 전체 CSS 선택기가 필요하지 않습니다. `select` 메서드에 값을 전달할 때 표시 텍스트 대신 기본 옵션 값을 전달해야 합니다.

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하여 무작위 옵션을 선택할 수 있습니다.

```php
$browser->select('size');
```

`select` 메서드의 두 번째 인수로 배열을 제공하면 메서드에 여러 옵션을 선택하도록 지시할 수 있습니다.

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스 입력을 "체크"하려면 `check` 메소드를 사용할 수 있습니다. 다른 많은 입력 관련 방법과 마찬가지로 전체 CSS 선택기가 필요하지 않습니다. CSS 선택기와 일치하는 항목을 찾을 수 없는 경우 Dusk는 일치하는 `name` 속성이 있는 확인란을 검색합니다.

```php
$browser->check('terms');
```

`uncheck` 메소드는 체크박스 입력을 "선택 해제"하는 데 사용될 수 있습니다:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

`radio` 입력 옵션을 "선택"하려면 `radio` 방법을 사용할 수 있습니다. 다른 많은 입력 관련 방법과 마찬가지로 전체 CSS 선택기가 필요하지 않습니다. CSS 선택기 일치를 찾을 수 없는 경우 Dusk는 일치하는 `name` 및 `value` 속성을 사용하여 `radio` 입력을 검색합니다.

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부

`attach` 메소드는 `file` 입력 요소에 파일을 첨부하는 데 사용될 수 있습니다. 다른 많은 입력 관련 방법과 마찬가지로 전체 CSS 선택기가 필요하지 않습니다. CSS 선택기 일치를 찾을 수 없는 경우 Dusk는 일치하는 `name` 속성을 사용하여 `file` 입력을 검색합니다.

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 연결 기능을 사용하려면 서버에 `Zip` PHP 확장을 설치하고 활성화해야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기

`press` 메소드는 페이지의 버튼 요소를 클릭하는 데 사용될 수 있습니다. `press` 메소드에 제공된 인수는 버튼의 표시 텍스트 또는 CSS / Dusk 선택기일 수 있습니다.

```php
$browser->press('Login');
```

양식을 제출할 때 많은 애플리케이션은 양식 제출 버튼을 누른 후 양식 제출 버튼을 비활성화하고 양식 제출의 HTTP 요청이 완료되면 버튼을 다시 활성화합니다. 버튼을 누르고 버튼이 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메소드를 사용할 수 있습니다.

```php
// Press the button and wait a maximum of 5 seconds for it to be enabled...
$browser->pressAndWaitFor('Save');

// Press the button and wait a maximum of 1 second for it to be enabled...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭

링크를 클릭하려면 브라우저 인스턴스에서 `clickLink` 메소드를 사용할 수 있습니다. `clickLink` 메소드는 지정된 표시 텍스트가 있는 링크를 클릭합니다.

```php
$browser->clickLink($linkText);
```

`seeLink` 메소드를 사용하여 주어진 표시 텍스트가 포함된 링크가 페이지에 표시되는지 확인할 수 있습니다.

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이러한 메서드는 jQuery와 상호 작용합니다. 페이지에서 jQuery를 사용할 수 없는 경우 Dusk는 이를 페이지에 자동으로 삽입하여 테스트 기간 동안 사용할 수 있도록 합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용

`keys` 방법을 사용하면 일반적으로 `type` 방법에서 허용하는 것보다 지정된 요소에 더 복잡한 입력 시퀀스를 제공할 수 있습니다. 예를 들어, 값을 입력하는 동안 수정자 키를 누르도록 Dusk에 지시할 수 있습니다. 이 예에서는 주어진 선택기와 일치하는 요소에 `taylor`가 입력되는 동안 `shift` 키가 유지됩니다. `taylor`를 입력한 후에는 수정자 키 없이 `swift`가 입력됩니다.

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

`keys` 메소드의 또 다른 유용한 사용 사례는 애플리케이션의 기본 CSS 선택기에 "키보드 단축키" 조합을 보내는 것입니다.

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 모든 수정자 키는 `{}` 문자로 래핑되며 [GitHub에서 찾을 수 있는](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php) `Facebook\WebDriver\WebDriverKeys` 클래스에 정의된 상수와 일치합니다.

<a name="fluent-keyboard-interactions"></a>
#### 유창한 키보드 상호 작용

Dusk는 `withKeyboard` 메서드도 제공하므로 `Laravel\Dusk\Keyboard` 클래스를 통해 복잡한 키보드 상호 작용을 유창하게 수행할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type` 및 `pause` 메서드를 제공합니다.

```php
use Laravel\Dusk\Keyboard;

$browser->withKeyboard(function (Keyboard $keyboard) {
    $keyboard->press('c')
        ->pause(1000)
        ->release('c')
        ->type(['c', 'e', 'o']);
});
```

<a name="keyboard-macros"></a>
#### 키보드 매크로

테스트 스위트 전체에서 쉽게 재사용할 수 있는 사용자 지정 키보드 상호 작용을 정의하려면 `Keyboard` 클래스에서 제공하는 `macro` 메서드를 사용할 수 있습니다. 일반적으로 [프로바이더 서비스](/docs/12.x/providers) `boot` 메서드에서 이 메서드를 호출해야 합니다.

```php
<?php

namespace App\Providers;

use Facebook\WebDriver\WebDriverKeys;
use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Keyboard;
use Laravel\Dusk\OperatingSystem;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Keyboard::macro('copy', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'c',
            ]);

            return $this;
        });

        Keyboard::macro('paste', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'v',
            ]);

            return $this;
        });
    }
}
```

`macro` 함수는 이름을 첫 번째 인수로, 클로저를 두 번째 인수로 받아들입니다. 매크로의 클로저는 `Keyboard` 인스턴스의 메서드로 매크로를 호출할 때 실행됩니다.

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용

<a name="clicking-on-elements"></a>
#### 요소 클릭

`click` 메소드는 주어진 CSS 또는 Dusk 선택기와 일치하는 요소를 클릭하는 데 사용될 수 있습니다.

```php
$browser->click('.selector');
```

`clickAtXPath` 메소드는 주어진 XPath 표현과 일치하는 요소를 클릭하는 데 사용될 수 있습니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메소드는 브라우저의 볼 수 있는 영역을 기준으로 지정된 좌표 쌍에서 맨 위 요소를 클릭하는 데 사용할 수 있습니다.

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메소드를 사용하여 마우스 더블 클릭을 시뮬레이션할 수 있습니다.

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick` 메소드를 사용하여 마우스 오른쪽 버튼 클릭을 시뮬레이션할 수 있습니다.

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` 메서드를 사용하면 마우스 버튼을 클릭하고 누르고 있는 모습을 시뮬레이션할 수 있습니다. `releaseMouse` 메서드에 대한 후속 호출은 이 동작을 취소하고 마우스 버튼을 놓습니다.

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick` 메소드는 브라우저 내에서 `ctrl+click` 이벤트를 시뮬레이션하는 데 사용될 수 있습니다.

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스오버

`mouseover` 메소드는 주어진 CSS 또는 Dusk 선택기와 일치하는 요소 위로 마우스를 이동해야 할 때 사용할 수 있습니다.

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메소드는 주어진 선택기와 일치하는 요소를 다른 요소로 드래그하는 데 사용될 수 있습니다.

```php
$browser->drag('.from-selector', '.to-selector');
```

또는 요소를 한 방향으로 끌 수도 있습니다.

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

마지막으로, 주어진 오프셋으로 요소를 드래그할 수 있습니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 대화상자

Dusk는 JavaScript 대화 상자와 상호 작용하는 다양한 방법을 제공합니다. 예를 들어 `waitForDialog` 메서드를 사용하여 JavaScript 대화 상자가 나타날 때까지 기다릴 수 있습니다. 이 메소드는 대화 상자가 나타날 때까지 기다려야 하는 시간(초)을 나타내는 선택적 인수를 허용합니다.

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메소드는 대화상자가 표시되었고 주어진 메시지를 포함하고 있음을 확인하는 데 사용될 수 있습니다:

```php
$browser->assertDialogOpened('Dialog message');
```

JavaScript 대화 상자에 프롬프트가 포함된 경우 `typeInDialog` 메서드를 사용하여 프롬프트에 값을 입력할 수 있습니다.

```php
$browser->typeInDialog('Hello World');
```

"확인" 버튼을 클릭하여 열려 있는 JavaScript 대화 상자를 닫으려면 `acceptDialog` 메서드를 호출하면 됩니다.

```php
$browser->acceptDialog();
```

"취소" 버튼을 클릭하여 열려 있는 JavaScript 대화 상자를 닫으려면 `dismissDialog` 메서드를 호출하면 됩니다.

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호 작용

iframe 내의 요소와 상호 작용해야 하는 경우 `withinFrame` 메서드를 사용할 수 있습니다. `withinFrame` 메소드에 제공된 클로저 내에서 발생하는 모든 요소 상호 작용은 지정된 iframe의 컨텍스트로 범위가 지정됩니다.

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 범위 지정 선택기

때로는 주어진 선택기 내에서 모든 작업의 ​​범위를 지정하면서 여러 작업을 수행하고 싶을 수도 있습니다. 예를 들어, 일부 텍스트가 표에만 존재한다고 주장한 다음 해당 표 내의 버튼을 클릭할 수 있습니다. 이를 수행하려면 `with` 메소드를 사용할 수 있습니다. `with` 메소드에 제공된 클로저 내에서 수행되는 모든 작업의 ​​범위는 원래 선택기로 지정됩니다.

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

때때로 현재 범위 외부에서 어설션을 실행해야 할 수도 있습니다. 이를 수행하려면 `elsewhere` 및 `elsewhereWhenAvailable` 메소드를 사용할 수 있습니다.

```php
$browser->with('.table', function (Browser $table) {
    // Current scope is `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소를 기다리는 중

JavaScript를 광범위하게 사용하는 애플리케이션을 테스트할 때 테스트를 진행하기 전에 특정 요소나 데이터를 사용할 수 있을 때까지 "대기"해야 하는 경우가 많습니다. Dusk는 이것을 아주 쉽게 만듭니다. 다양한 방법을 사용하여 요소가 페이지에 표시될 때까지 기다리거나 특정 JavaScript 표현식이 `true`로 평가될 때까지 기다릴 수도 있습니다.

<a name="waiting"></a>
#### 대기 중

지정된 밀리초 동안 테스트를 일시 중지해야 하는 경우 `pause` 메서드를 사용하세요.

```php
$browser->pause(1000);
```

주어진 조건이 `true`인 경우에만 테스트를 일시 중지해야 하는 경우 `pauseIf` 메서드를 사용하세요.

```php
$browser->pauseIf(App::environment('production'), 1000);
```

마찬가지로, 주어진 조건이 `true`가 아닌 이상 테스트를 일시 중지해야 하는 경우 `pauseUnless` 메서드를 사용할 수 있습니다.

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 선택자를 기다리는 중

`waitFor` 메소드는 주어진 CSS 또는 Dusk 선택기와 일치하는 요소가 페이지에 표시될 때까지 테스트 실행을 일시 중지하는 데 사용될 수 있습니다. 기본적으로 예외가 발생하기 전에 최대 5초 동안 테스트가 일시 중지됩니다. 필요한 경우 사용자 지정 시간 제한 임계값을 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
// Wait a maximum of five seconds for the selector...
$browser->waitFor('.selector');

// Wait a maximum of one second for the selector...
$browser->waitFor('.selector', 1);
```

주어진 선택자와 일치하는 요소가 주어진 텍스트를 포함할 때까지 기다릴 수도 있습니다:

```php
// Wait a maximum of five seconds for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World');

// Wait a maximum of one second for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

또한 주어진 선택자와 일치하는 요소가 페이지에서 누락될 때까지 기다릴 수도 있습니다.

```php
// Wait a maximum of five seconds until the selector is missing...
$browser->waitUntilMissing('.selector');

// Wait a maximum of one second until the selector is missing...
$browser->waitUntilMissing('.selector', 1);
```

또는 주어진 선택기와 일치하는 요소가 활성화되거나 비활성화될 때까지 기다릴 수 있습니다.

```php
// Wait a maximum of five seconds until the selector is enabled...
$browser->waitUntilEnabled('.selector');

// Wait a maximum of one second until the selector is enabled...
$browser->waitUntilEnabled('.selector', 1);

// Wait a maximum of five seconds until the selector is disabled...
$browser->waitUntilDisabled('.selector');

// Wait a maximum of one second until the selector is disabled...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 사용 가능한 경우 범위 지정 선택기

때로는 주어진 선택기와 일치하는 요소가 나타날 때까지 기다린 다음 해당 요소와 상호 작용하기를 원할 수도 있습니다. 예를 들어, 모달 창을 사용할 수 있을 때까지 기다린 다음 모달 내에서 "확인" 버튼을 누를 수 있습니다. 이를 달성하기 위해 `whenAvailable` 메소드를 사용할 수 있습니다. 지정된 클로저 내에서 수행되는 모든 요소 작업의 범위는 원래 선택기로 지정됩니다.

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 문자를 기다리는 중

`waitForText` 메소드는 주어진 텍스트가 페이지에 표시될 때까지 기다리는 데 사용될 수 있습니다:

```php
// Wait a maximum of five seconds for the text...
$browser->waitForText('Hello World');

// Wait a maximum of one second for the text...
$browser->waitForText('Hello World', 1);
```

표시된 텍스트가 페이지에서 제거될 때까지 기다리려면 `waitUntilMissingText` 메소드를 사용할 수 있습니다.

```php
// Wait a maximum of five seconds for the text to be removed...
$browser->waitUntilMissingText('Hello World');

// Wait a maximum of one second for the text to be removed...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크를 기다리는 중

`waitForLink` 메소드는 주어진 링크 텍스트가 페이지에 표시될 때까지 기다리는 데 사용될 수 있습니다:

```php
// Wait a maximum of five seconds for the link...
$browser->waitForLink('Create');

// Wait a maximum of one second for the link...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력을 기다리는 중

`waitForInput` 메소드는 주어진 입력 필드가 페이지에 표시될 때까지 기다리는 데 사용할 수 있습니다.

```php
// Wait a maximum of five seconds for the input...
$browser->waitForInput($field);

// Wait a maximum of one second for the input...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치를 기다리는 중

`$browser->assertPathIs('/home')`와 같은 경로 어설션을 만들 때 `window.location.pathname`가 비동기적으로 업데이트되면 어설션이 실패할 수 있습니다. `waitForLocation` 메소드를 사용하여 위치가 주어진 값이 될 때까지 기다릴 수 있습니다:

```php
$browser->waitForLocation('/secret');
```

`waitForLocation` 메서드를 사용하여 현재 창 위치가 정규화된 URL가 될 때까지 기다릴 수도 있습니다.

```php
$browser->waitForLocation('https://example.com/path');
```

[named 라우트's](/docs/12.x/routing#named-routes) 위치를 기다릴 수도 있습니다.

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침을 기다리는 중

작업을 수행한 후 페이지가 다시 로드될 때까지 기다려야 하는 경우 `waitForReload` 메서드를 사용하세요.

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

일반적으로 버튼을 클릭한 후 페이지가 다시 로드될 때까지 기다려야 하므로 편의를 위해 `clickAndWaitForReload` 메서드를 사용할 수 있습니다.

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식을 기다리는 중

때로는 주어진 JavaScript 표현식이 `true`로 평가될 때까지 테스트 실행을 일시 중지하고 싶을 수도 있습니다. `waitUntil` 방법을 사용하면 이 작업을 쉽게 수행할 수 있습니다. 이 메서드에 표현식을 전달할 때 `return` 키워드나 끝 세미콜론을 포함할 필요가 없습니다.

```php
// Wait a maximum of five seconds for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0');

// Wait a maximum of one second for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식을 기다리는 중

`waitUntilVue` 및 `waitUntilVueIsNot` 메소드는 [Vue 컴포넌트](https://vuejs.org) 속성이 지정된 값을 가질 때까지 기다리는 데 사용할 수 있습니다.

```php
// Wait until the component attribute contains the given value...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// Wait until the component attribute doesn't contain the given value...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트를 기다리는 중

`waitForEvent` 메서드를 사용하면 JavaScript 이벤트가 발생할 때까지 테스트 실행을 일시 중지할 수 있습니다.

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 `body` 요소인 현재 범위에 연결됩니다. 범위가 지정된 선택기를 사용하는 경우 이벤트 리스너가 일치하는 요소에 연결됩니다.

```php
$browser->with('iframe', function (Browser $iframe) {
    // Wait for the iframe's load event...
    $iframe->waitForEvent('load');
});
```

이벤트 리스너를 특정 요소에 연결하기 위해 `waitForEvent` 메서드의 두 번째 인수로 선택기를 제공할 수도 있습니다.

```php
$browser->waitForEvent('load', '.selector');
```

`document` 및 `window` 개체에서 이벤트를 기다릴 수도 있습니다.

```php
// Wait until the document is scrolled...
$browser->waitForEvent('scroll', 'document');

// Wait a maximum of five seconds until the window is resized...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백 대기 중

Dusk의 많은 "대기" 메서드는 기본 `waitUsing` 메서드에 의존합니다. 이 메소드를 직접 사용하여 주어진 클로저가 `true`를 반환할 때까지 기다릴 수 있습니다. `waitUsing` 메서드는 대기할 최대 시간(초), 클로저를 평가해야 하는 간격, 클로저 및 선택적 실패 메시지를 허용합니다.

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 뷰로 스크롤

때로는 요소가 브라우저의 볼 수 있는 영역 밖에 있기 때문에 요소를 클릭하지 못할 수도 있습니다. `scrollIntoView` 메소드는 주어진 선택기의 요소가 뷰 내에 있을 때까지 브라우저 창을 스크롤합니다.

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 수행할 수 있는 다양한 어설션을 제공합니다. 사용 가능한 모든 어설션은 아래 목록에 문서화되어 있습니다.

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[제목 주장](#assert-title)
[제목 포함 주장](#assert-title-contains)
[assertUrlIs](#assert-url-is)
[assertSchemeIs](#assert-scheme-is)
[assertSchemeIsNot](#assert-scheme-is-not)
[호스트가 다음과 같음](#assert-host-is)
[호스트가 아님을 주장](#assert-host-is-not)
[assertPortIs](#assert-port-is)
[assertPortIsNot](#assert-port-is-not)
[assertPathBeginsWith](#assert-path-begins-with)
[assertPathEndsWith](#assert-path-ends-with)
[assertPathContains](#assert-path-contains)
[경로 확인](#assert-path-is)
[경로가 아님을 주장](#assert-path-is-not)
[RouteIs 주장](#assert-route-is)
[QueryStringHas 주장](#assert-query-string-has)
[어설션쿼리문자열 누락](#assert-query-string-missing)
[assertFragmentIs](#assert-fragment-is)
[assertFragmentBeginsWith](#assert-fragment-begins-with)
[assertFragmentIsNot](#assert-fragment-is-not)
[쿠키 있음 주장](#assert-has-cookie)
[HasPlainCookie 주장](#assert-has-plain-cookie)
[쿠키누락 주장](#assert-cookie-missing)
[PlainCookieMissing 확인](#assert-plain-cookie-missing)
[쿠키값 주장](#assert-cookie-value)
[PlainCookie값 주장](#assert-plain-cookie-value)
[주장참조](#assert-see)
[참조하지 말라고 주장](#assert-dont-see)
[assertSeeIn](#assert-see-in)
[참조하지 말라고 주장](#assert-dont-see-in)
[AsertSeeAnythingIn](#assert-see-anything-in)
[AsertSeeNothingIn](#assert-see-nothing-in)
[assertCount](#assert-count)
[어설션스크립트](#assert-script)
[원본이 있음](#assert-source-has)
[어설션소스 누락](#assert-source-missing)
[링크 확인](#assert-see-link)
[링크를 보지 말라고 주장](#assert-dont-see-link)
[입력값 주장](#assert-input-value)
[assertInputValueIsNot](#assert-input-value-is-not)
[확인됨](#assert-checked)
[확인되지 않음 확인](#assert-not-checked)
[미정 주장](#assert-indeterminate)
[assertRadioSelected](#assert-radio-selected)
[assertRadioNotSelected](#assert-radio-not-selected)
[선택됨](#assert-selected)
[선택되지 않음 주장](#assert-not-selected)
[assertSelectHasOptions](#assert-select-has-options)
[MissingOptions 선택](#assert-select-missing-options)
[assertSelectHasOption](#assert-select-has-option)
[MissingOption 주장](#assert-select-missing-option)
[어설션값](#assert-value)
[assertValueIsNot](#assert-value-is-not)
[assert속성](#assert-attribute)
[assert속성누락](#assert-attribute-missing)
[assertAttributeContains](#assert-attribute-contains)
[assertAttributeDoesntContain](#assert-attribute-doesnt-contain)
[assertAria속성](#assert-aria-attribute)
[assertData속성](#assert-data-attribute)
[가시적 주장](#assert-visible)
[현재 주장](#assert-present)
[현재 존재하지 않음 주장](#assert-not-present)
[어설션누락](#assert-missing)
[assertInputPresent](#assert-input-present)
[입력 누락 주장](#assert-input-missing)
[assertDialogOpened](#assert-dialog-opened)
[어설션 활성화됨](#assert-enabled)
[비활성화됨](#assert-disabled)
[assertButton활성화](#assert-button-enabled)
[assertButton비활성화됨](#assert-button-disabled)
[집중된 주장](#assert-focused)
[집중되지 않음 주장](#assert-not-focused)
[인증됨](#assert-authenticated)
[assertGuest](#assert-guest)
[인증된 것으로 주장](#assert-authenticated-as)
[assertVue](#assert-vue)
[VueIsNot 주장](#assert-vue-is-not)
[assertVueContains](#assert-vue-contains)
[VueDoesntContain 주장](#assert-vue-doesnt-contain)

</div>

<a name="assert-title"></a>
#### 주장제목

페이지 제목이 주어진 텍스트와 일치하는지 확인:

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### 주장제목은 다음을 포함합니다

페이지 제목에 주어진 텍스트가 포함되어 있는지 확인:

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### 주장UrlIs

현재 URL(쿼리 문자열 제외)가 주어진 문자열과 일치하는지 확인:

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### AssertSchemeIs

현재 URL 체계가 주어진 체계와 일치하는지 확인:

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### AssertSchemeIsNot

현재 URL 체계가 주어진 체계와 일치하지 않는지 확인:

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### 주장HostIs

현재 URL 호스트가 주어진 호스트와 일치하는지 확인:

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### 주장HostIsNot

현재 URL 호스트가 주어진 호스트와 일치하지 않는지 확인:

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### 주장PortIs

현재 URL 포트가 지정된 포트와 일치하는지 확인합니다.

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### 포트가 아님을 주장

현재 URL 포트가 주어진 포트와 일치하지 않는지 확인:

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### AssertPathBeginsWith

현재 URL 경로가 주어진 경로로 시작하는지 확인:

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### AssertPathEndsWith

현재 URL 경로가 주어진 경로로 끝나는지 확인:

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### AssertPathContains

현재 URL 경로에 주어진 경로가 포함되어 있는지 확인:

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### AssertPathIs

현재 경로가 주어진 경로와 일치하는지 확인:

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### AssertPathIsNot

현재 경로가 주어진 경로와 일치하지 않는지 확인:

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### AssertRouteIs

현재 URL가 주어진 [라우트's](/docs/12.x/routing#named-routes) URL와 일치하는지 확인합니다.

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### 주장QueryStringHas

주어진 쿼리 문자열 매개변수가 존재하는지 확인:

```php
$browser->assertQueryStringHas($name);
```

주어진 쿼리 문자열 매개변수가 존재하고 주어진 값을 가지고 있는지 확인:

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### AssertQueryString누락

주어진 쿼리 문자열 매개변수가 누락되었는지 확인:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### 주장FragmentIs

URL의 현재 해시 조각이 주어진 조각과 일치하는지 확인합니다.

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### 주장FragmentBeginsWith

URL의 현재 해시 조각이 주어진 조각으로 시작하는지 확인합니다.

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### 주장FragmentIsNot

URL의 현재 해시 조각이 주어진 조각과 일치하지 않는지 확인:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### AssertHasCookie

주어진 암호화된 쿠키가 존재하는지 확인:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### AssertHasPlainCookie

주어진 암호화되지 않은 쿠키가 존재하는지 확인:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### 어설션쿠키누락

주어진 암호화된 쿠키가 존재하지 않는지 확인:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### 주장일반쿠키누락

주어진 암호화되지 않은 쿠키가 존재하지 않는지 확인:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### AssertCookieValue

암호화된 쿠키가 주어진 값을 가지고 있는지 확인:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### AssertPlainCookieValue

암호화되지 않은 쿠키가 주어진 값을 가지고 있는지 확인:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### 주장참조

주어진 텍스트가 페이지에 존재하는지 확인:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### 주장하지 마세요.

주어진 텍스트가 페이지에 존재하지 않는지 확인:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### 주장하다SeeIn

주어진 텍스트가 선택자 내에 존재하는지 확인:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### 주장하지 마세요.

주어진 텍스트가 선택자 내에 존재하지 않는지 확인:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### 주장아무것도보고

선택기 내에 텍스트가 있는지 확인합니다.

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### 주장아무것도보이지 않음

선택기 내에 텍스트가 없는지 확인:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-count"></a>
#### 주장개수

주어진 선택자와 일치하는 요소가 지정된 횟수만큼 나타나는지 확인:

```php
$browser->assertCount($selector, $count);
```

<a name="assert-script"></a>
#### 주장스크립트

주어진 JavaScript 표현식이 주어진 값으로 평가되는지 확인:

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### AssertSourceHas

주어진 소스 코드가 페이지에 존재하는지 확인:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### AssertSource누락

주어진 소스 코드가 페이지에 존재하지 않는지 확인:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### 주장참조링크

주어진 링크가 페이지에 존재하는지 확인:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### 주장하지 마세요링크

해당 링크가 페이지에 존재하지 않는지 확인:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### 주장입력값

주어진 입력 필드가 주어진 값을 가지고 있는지 확인:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### AssertInputValueIsNot

주어진 입력 필드가 주어진 값을 가지고 있지 않은지 확인:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### 주장확인됨

주어진 체크박스가 선택되어 있는지 확인:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### AssertNotChecked

주어진 체크박스가 선택되어 있지 않은지 확인:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### 확정되지 않은 주장

주어진 체크박스가 불확정 상태인지 확인:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### AssertRadioSelected

주어진 라디오 필드가 선택되었는지 확인:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### AssertRadioNotSelected

주어진 라디오 필드가 선택되지 않았는지 확인:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### 선택됨 주장

주어진 드롭다운에 주어진 값이 선택되어 있는지 확인:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### 선택되지 않음 주장

주어진 드롭다운에 주어진 값이 선택되어 있지 않은지 확인:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### AssertSelectHasOptions

주어진 값의 배열을 선택할 수 있는지 확인:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### AssertSelectMissingOptions

주어진 값의 배열을 선택할 수 없는지 확인:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### AssertSelectHasOption

주어진 필드에서 주어진 값을 선택할 수 있는지 확인:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### AssertSelectMissingOption

주어진 값을 선택할 수 없는지 확인:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### 주장값

주어진 선택자와 일치하는 요소가 주어진 값을 가지고 있는지 확인:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### AssertValueIsNot

주어진 선택자와 일치하는 요소가 주어진 값을 가지고 있지 않은지 확인:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### 주장속성

주어진 선택자와 일치하는 요소가 제공된 속성에 주어진 값을 가지고 있는지 확인:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### AssertAttributeMissing

주어진 선택자와 일치하는 요소에 제공된 속성이 누락되었는지 확인:

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### AssertAttributeContains

주어진 선택자와 일치하는 요소가 제공된 속성에 주어진 값을 포함하는지 확인:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### AssertAttributeDoesntContain

주어진 선택자와 일치하는 요소가 제공된 속성에 주어진 값을 포함하지 않는지 확인:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### 주장Aria속성

주어진 선택자와 일치하는 요소가 제공된 aria 속성에 주어진 값을 가지고 있는지 확인:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>` 마크업이 있는 경우 다음과 같이 `aria-label` 속성에 대해 어설션할 수 있습니다.

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### 주장데이터속성

주어진 선택자와 일치하는 요소가 제공된 데이터 속성에 주어진 값을 가지고 있는지 확인:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>` 마크업이 있는 경우 다음과 같이 `data-label` 속성에 대해 어설션할 수 있습니다.

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### 주장가시적

주어진 선택자와 일치하는 요소가 표시되는지 확인:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### 주장현재

주어진 선택자와 일치하는 요소가 소스에 존재하는지 확인:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### AssertNotPresent

주어진 선택자와 일치하는 요소가 소스에 존재하지 않는지 확인:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### 주장누락

주어진 선택자와 일치하는 요소가 표시되지 않는지 확인:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### 주장입력현재

주어진 이름을 가진 입력이 존재하는지 확인:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### 주장입력누락

주어진 이름을 가진 입력이 소스에 존재하지 않는지 확인:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### 주장대화상자열림

주어진 메시지가 있는 JavaScript 대화 상자가 열렸는지 확인:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### 주장 활성화됨

주어진 필드가 활성화되어 있는지 확인:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### 주장 비활성화됨

주어진 필드가 비활성화되어 있는지 확인:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### 주장버튼 활성화됨

주어진 버튼이 활성화되어 있는지 확인:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### 주장버튼이 비활성화되었습니다.

주어진 버튼이 비활성화되었는지 확인:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### 주장집중

주어진 필드에 포커스가 있는지 확인:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### AssertNotFocused

주어진 필드에 포커스가 없는지 확인:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### 주장인증됨

사용자가 인증되었는지 확인합니다.

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### 주장게스트

사용자가 인증되지 않았는지 확인:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### AssertAuthenticatedAs

사용자가 주어진 사용자로 인증되었는지 확인:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### 주장Vue

Dusk를 사용하면 [Vue 컴포넌트](https://vuejs.org) 데이터의 상태에 대한 어설션도 수행할 수 있습니다. 예를 들어 애플리케이션에 다음 Vue 컴포넌트가 포함되어 있다고 가정해 보겠습니다.

// HTML...

<profile 황혼="프로필 컴포넌트"></profile>

// Component Definition...

Vue.comComponent('프로필', {
        템플릿: '<div>{{ user.name }}</div>',

데이터: 함수 () {
            반환 {
                사용자: {
                    이름: '테일러'
                }
            };
        }
    });

다음과 같이 Vue 구성요소의 상태를 주장할 수 있습니다.

```php tab=Pest
test('vue', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
});
```

```php tab=PHPUnit
/**
 * A basic Vue test example.
 */
public function test_vue(): void
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
}
```

<a name="assert-vue-is-not"></a>
#### VueIsNot 주장

주어진 Vue 구성요소 데이터 속성이 주어진 값과 일치하지 않는지 확인:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### VueContains 주장

주어진 Vue 구성요소 데이터 속성이 배열이고 주어진 값을 포함하는지 확인:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### VueDoesntContain 주장

주어진 Vue 구성요소 데이터 속성이 배열이고 주어진 값을 포함하지 않는지 확인:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

때때로 테스트에서는 여러 가지 복잡한 작업을 순서대로 수행해야 합니다. 이로 인해 테스트를 읽고 이해하기가 더 어려워질 수 있습니다. Dusk 페이지를 사용하면 단일 메서드를 통해 특정 페이지에서 수행할 수 있는 표현 작업을 정의할 수 있습니다. 또한 페이지를 사용하면 애플리케이션이나 단일 페이지에 대한 공통 선택기에 대한 바로 가기를 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성

페이지 개체를 생성하려면 `dusk:page` Artisan 명령을 실행합니다. 모든 페이지 개체는 애플리케이션의 `tests/Browser/Pages` 디렉터리에 배치됩니다.

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 구성

기본적으로 페이지에는 `url`, `assert` 및 `elements`의 세 가지 방법이 있습니다. 이제 `url` 및 `assert` 방법에 대해 논의하겠습니다. `elements` 방법은 [아래에서 더 자세히 논의](#shorthand-selectors)됩니다.

<a name="the-url-method"></a>
#### `url` 방법

`url` 메소드는 페이지를 나타내는 URL의 경로를 반환해야 합니다. Dusk는 브라우저에서 페이지를 탐색할 때 이 URL를 사용합니다.

```php
/**
 * Get the URL for the page.
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 방법

`assert` 메소드는 브라우저가 실제로 주어진 페이지에 있는지 확인하는 데 필요한 어설션을 만들 수 있습니다. 실제로 이 메서드 내에 아무것도 배치할 필요는 없습니다. 그러나 원한다면 이러한 주장을 자유롭게 할 수 있습니다. 다음 어설션은 페이지를 탐색할 때 자동으로 실행됩니다.

```php
/**
 * Assert that the browser is on the page.
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동

페이지가 정의되면 `visit` 메소드를 사용하여 해당 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

때로는 특정 페이지에 이미 있고 페이지의 선택기와 메소드를 현재 테스트 컨텍스트에 "로드"해야 할 수도 있습니다. 이는 버튼을 누르고 명시적으로 해당 페이지로 이동하지 않고 지정된 페이지로 리디렉션될 때 일반적입니다. 이 상황에서는 `on` 메소드를 사용하여 페이지를 로드할 수 있습니다.

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 속기 선택자

페이지 클래스 내의 `elements` 메소드를 사용하면 페이지의 CSS 선택기에 대해 빠르고 기억하기 쉬운 단축키를 정의할 수 있습니다. 예를 들어, 애플리케이션 로그인 페이지의 "이메일" 입력 필드에 대한 바로가기를 정의해 보겠습니다.

```php
/**
 * Get the element shortcuts for the page.
 *
 * @return array<string, string>
 */
public function elements(): array
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

단축키가 정의되면 일반적으로 전체 CSS 선택기를 사용하는 곳 어디에서나 단축 선택기를 사용할 수 있습니다.

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 단축 선택기

Dusk를 설치하면 기본 `Page` 클래스가 `tests/Browser/Pages` 디렉터리에 배치됩니다. 이 클래스에는 애플리케이션 전체의 모든 페이지에서 사용할 수 있는 전역 단축 선택기를 정의하는 데 사용할 수 있는 `siteElements` 메서드가 포함되어 있습니다.

```php
/**
 * Get the global element shortcuts for the site.
 *
 * @return array<string, string>
 */
public static function siteElements(): array
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
### 페이지 방법

페이지에 정의된 기본 방법 외에도 테스트 전반에 걸쳐 사용할 수 있는 추가 방법을 정의할 수 있습니다. 예를 들어 음악 관리 애플리케이션을 구축한다고 가정해 보겠습니다. 애플리케이션의 한 페이지에 대한 일반적인 작업은 재생 목록을 만드는 것일 수 있습니다. 각 테스트에서 재생 목록을 생성하는 로직을 다시 작성하는 대신 페이지 클래스에 `createPlaylist` 메서드를 정의할 수 있습니다.

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // Other page methods...

    /**
     * Create a new playlist.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

메소드가 정의되면 페이지를 활용하는 모든 테스트 내에서 이를 사용할 수 있습니다. 브라우저 인스턴스는 자동으로 사용자 지정 페이지 메소드의 첫 번째 인수로 전달됩니다.

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 구성요소 (Components)

컴포넌트는 Dusk의 "페이지 개체"와 유사하지만 탐색 모음이나 알림 창과 같이 애플리케이션 전체에서 재사용되는 UI 및 기능을 위한 것입니다. 따라서 컴포넌트는 특정 URL에 바인딩되지 않습니다.

<a name="generating-components"></a>
### 구성요소 생성

구성요소를 생성하려면 `dusk:component` Artisan 명령을 실행합니다. 새 구성요소는 `tests/Browser/Components` 디렉토리에 배치됩니다.

```shell
php artisan dusk:component DatePicker
```

위에 표시된 대로 "날짜 선택기"는 애플리케이션 전체의 다양한 페이지에 존재할 수 있는 컴포넌트의 예입니다. 테스트 모음 전체에 걸쳐 수십 개의 테스트에서 날짜를 선택하기 위해 브라우저 자동화 로직을 수동으로 작성하는 것은 번거로울 수 있습니다. 대신 날짜 선택기를 나타내는 Dusk 컴포넌트를 정의하여 해당 논리를 컴포넌트 내에 캡슐화할 수 있습니다.

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * Get the root selector for the component.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * Assert that the browser page contains the component.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * Get the element shortcuts for the component.
     *
     * @return array<string, string>
     */
    public function elements(): array
    {
        return [
            '@date-field' => 'input.datepicker-input',
            '@year-list' => 'div > div.datepicker-years',
            '@month-list' => 'div > div.datepicker-months',
            '@day-list' => 'div > div.datepicker-days',
        ];
    }

    /**
     * Select the given date.
     */
    public function selectDate(Browser $browser, int $year, int $month, int $day): void
    {
        $browser->click('@date-field')
            ->within('@year-list', function (Browser $browser) use ($year) {
                $browser->click($year);
            })
            ->within('@month-list', function (Browser $browser) use ($month) {
                $browser->click($month);
            })
            ->within('@day-list', function (Browser $browser) use ($day) {
                $browser->click($day);
            });
    }
}
```

<a name="using-components"></a>
### 구성요소 사용

컴포넌트가 정의되면 모든 테스트의 날짜 선택기 내에서 날짜를 쉽게 선택할 수 있습니다. 그리고 날짜를 선택하는 데 필요한 로직이 변경되면 컴포넌트만 업데이트하면 됩니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->within(new DatePicker, function (Browser $browser) {
                $browser->selectDate(2019, 1, 30);
            })
            ->assertSee('January');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    /**
     * A basic component test example.
     */
    public function test_basic_example(): void
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                ->within(new DatePicker, function (Browser $browser) {
                    $browser->selectDate(2019, 1, 30);
                })
                ->assertSee('January');
        });
    }
}
```

`component` 메소드는 주어진 컴포넌트로 범위가 지정된 브라우저 인스턴스를 검색하는 데 사용될 수 있습니다.

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적인 통합 (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk 연속 통합 구성에서는 Laravel 애플리케이션이 포트 8000에 내장된 PHP 개발 서버를 사용하여 제공될 것으로 예상합니다. 따라서 계속하기 전에 연속 통합 환경에 `APP_URL` 환경 변수 값 `http://127.0.0.1:8000`가 있는지 확인해야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### 헤로쿠 CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 다음 Google Chrome 빌드팩과 스크립트를 Heroku `app.json` 파일에 추가하세요.

```json
{
  "environments": {
    "test": {
      "buildpacks": [
        { "url": "heroku/php" },
        { "url": "https://github.com/heroku/heroku-buildpack-chrome-for-testing" }
      ],
      "scripts": {
        "test-setup": "cp .env.testing .env",
        "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux --port=9515 > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk"
      }
    }
  }
}
```

<a name="running-tests-on-travis-ci"></a>
### 트래비스 CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 다음 `.travis.yml` 구성을 사용하세요. Travis CI는 그래픽 환경이 아니기 때문에 Chrome 브라우저를 실행하려면 몇 가지 추가 단계를 수행해야 합니다. 또한 `php artisan serve`를 사용하여 PHP의 내장 웹 서버를 시작합니다.

```yaml
language: php

php:
  - 8.2

addons:
  chrome: stable

install:
  - cp .env.testing .env
  - travis_retry composer install --no-interaction --prefer-dist
  - php artisan key:generate
  - php artisan dusk:chrome-driver

before_script:
  - google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost &
  - php artisan serve --no-reload &

script:
  - php artisan dusk
```

<a name="running-tests-on-github-actions"></a>
### GitHub 작업

[GitHub 작업](https://github.com/features/actions)을 사용하여 Dusk 테스트를 실행하는 경우 다음 구성 파일을 시작점으로 사용할 수 있습니다. TravisCI와 마찬가지로 `php artisan serve` 명령을 사용하여 PHP의 내장 웹 서버를 시작합니다.

```yaml
name: CI
on: [push]
jobs:

  dusk-php:
    runs-on: ubuntu-latest
    env:
      APP_URL: "http://127.0.0.1:8000"
      DB_USERNAME: root
      DB_PASSWORD: root
      MAIL_MAILER: log
    steps:
      - uses: actions/checkout@v5
      - name: Prepare The Environment
        run: cp .env.example .env
      - name: Create Database
        run: |
          sudo systemctl start mysql
          mysql --user="root" --password="root" -e "CREATE DATABASE \`my-database\` character set UTF8mb4 collate utf8mb4_bin;"
      - name: Install Composer Dependencies
        run: composer install --no-progress --prefer-dist --optimize-autoloader
      - name: Generate Application Key
        run: php artisan key:generate
      - name: Upgrade Chrome Driver
        run: php artisan dusk:chrome-driver --detect
      - name: Start Chrome Driver
        run: ./vendor/laravel/dusk/bin/chromedriver-linux --port=9515 &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        run: php artisan dusk
      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: tests/Browser/screenshots
      - name: Upload Console Logs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: console
          path: tests/Browser/console
```

<a name="running-tests-on-chipper-ci"></a>
### 치퍼 CI

[Chipper CI](https://chipperci.com)를 사용하여 Dusk 테스트를 실행하는 경우 다음 구성 파일을 시작점으로 사용할 수 있습니다. 요청을 수신할 수 있도록 PHP의 내장 서버를 사용하여 Laravel을 실행합니다.

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Include Chrome in the build environment
services:
  - dusk

# Build all commits
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate

      # Create a dusk env file, ensuring APP_URL uses BUILD_HOST
      cp -v .env .env.dusk.ci
      sed -i "s@APP_URL=.*@APP_URL=http://$BUILD_HOST:8000@g" .env.dusk.ci

  - name: Compile Assets
    cmd: |
      npm ci --no-audit
      npm run build

  - name: Browser Tests
    cmd: |
      php -S [::0]:8000 -t public 2>server.log &
      sleep 2
      php artisan dusk:chrome-driver $CHROME_DRIVER
      php artisan dusk --env=ci
```

데이터베이스 사용 방법을 포함하여 Chipper CI에서 Dusk 테스트를 실행하는 방법에 대해 자세히 알아보려면 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참조하세요.
