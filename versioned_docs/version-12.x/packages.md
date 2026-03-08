# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 참고 사항](#a-note-on-facades)
- [패키지 자동 발견](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [라우트](#routes)
    - [마이그레이션](#migrations)
    - [언어 파일](#language-files)
    - [뷰](#views)
    - [뷰 컴포넌트](#view-components)
    - ["About" 아티즌 명령어](#about-artisan-command)
- [명령어](#commands)
    - [최적화 명령어](#optimize-commands)
    - [재로드 명령어](#reload-commands)
- [퍼블릭 에셋](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)처럼 날짜를 다루기 위한 훌륭한 방법일 수도 있고, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연동할 수 있도록 해주는 패키지일 수도 있습니다.

패키지에는 여러 종류가 있습니다. 어떤 패키지는 독립 실행형(stand-alone)으로, 모든 PHP 프레임워크에서 동작할 수 있습니다. Carbon과 Pest가 그 예시입니다. 이런 패키지들도 `composer.json` 파일에 require하여 Laravel에서 사용할 수 있습니다.

반대로, 일부 패키지는 오직 Laravel에서 사용하기 위한 목적으로 만들어집니다. 이런 패키지에는 Laravel 애플리케이션을 확장하는 데 적합한 라우트, 컨트롤러, 뷰, 설정 등이 포함돼 있을 수 있습니다. 이 가이드는 주로 Laravel에 특화된 패키지를 개발하는 방법을 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 참고 사항

Laravel 애플리케이션을 개발할 때는 contracts나 facades 모두 테스트 가능성 측면에서 거의 동일하므로 어느 것을 사용해도 큰 문제가 되지 않습니다. 그러나 패키지를 개발할 때는 Laravel의 모든 테스트 헬퍼를 사용할 수 없는 경우가 많습니다. 패키지의 테스트를 일반적인 Laravel 애플리케이션 안에 설치된 것처럼 작성하려면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 자동 발견 (Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 Laravel에서 로드해야 하는 서비스 프로바이더 목록이 들어 있습니다. 하지만 사용자에게 서비스 프로바이더를 직접 목록에 추가하도록 요구하지 않고, 패키지의 `composer.json` 파일 `extra` 섹션에 프로바이더를 정의해두면 Laravel이 자동으로 이를 로드하도록 할 수 있습니다. 서비스 프로바이더 뿐 아니라 등록하고 싶은 [파사드](/docs/12.x/facades)도 함께 지정할 수 있습니다:

```json
"extra": {
    "laravel": {
        "providers": [
            "Barryvdh\\Debugbar\\ServiceProvider"
        ],
        "aliases": {
            "Debugbar": "Barryvdh\\Debugbar\\Facade"
        }
    }
},
```

패키지가 자동 발견에 맞게 구성된 경우, Laravel은 패키지가 설치되는 즉시 서비스 프로바이더와 파사드를 자동으로 등록하여 사용자에게 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 자동 발견 비활성화

패키지를 사용하는 입장에서 해당 패키지의 자동 발견을 끄고 싶다면, 애플리케이션의 `composer.json` 파일 `extra` 섹션에 패키지명을 추가하면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

애플리케이션의 `dont-discover` 항목에서 `*` 문자를 사용하면 모든 패키지의 자동 발견을 비활성화할 수도 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a name="service-providers"></a>
## 서비스 프로바이더 (Service Providers)

[서비스 프로바이더](/docs/12.x/providers)는 패키지와 Laravel을 연결해주는 중개자 역할을 합니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/12.x/container)에 다양한 객체를 바인딩하고, 패키지의 뷰, 설정, 언어 파일 등 리소스의 위치를 Laravel에 알려주는 책임을 집니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장하며, `register`와 `boot`라는 두 가지 메서드를 가집니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으므로, 이를 패키지 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 자세히 알고 싶다면 [관련 문서](/docs/12.x/providers)를 참고하세요.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 (Configuration)

일반적으로 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시해주어야 합니다. 이를 통해 패키지 사용자가 기본 설정 값을 쉽게 오버라이드할 수 있습니다. 설정 파일을 퍼블리시할 수 있도록 하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면 설정 파일이 지정된 위치에 복사됩니다. 설정 파일이 퍼블리시된 후에는 일반 설정 파일처럼 값을 읽을 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일 내에 클로저를 정의하지 마세요. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정

패키지의 설정 파일을 애플리케이션에 퍼블리시된 복사본과 병합(merge)할 수도 있습니다. 이렇게 하면 사용자는 오버라이드하고 싶은 옵션만 설정 파일에 정의해 두면 됩니다. 설정 값 병합은 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하면 됩니다.

`mergeConfigFrom` 메서드는 첫 번째 인수로 패키지 설정 파일 경로, 두 번째 인수로 애플리케이션에서 사용할 설정 이름을 받습니다:

```php
/**
 * Register any package services.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!WARNING]
> 이 메서드는 설정 배열의 1단계까지만 병합합니다. 사용자가 다차원 배열 설정을 부분적으로 정의할 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 사용하여 로드할 수 있습니다. 이 메서드는 애플리케이션의 라우트가 캐시되어 있다면 라우트 파일을 불러오지 않으므로 효율적입니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
### 마이그레이션 (Migrations)

패키지에 [데이터베이스 마이그레이션](/docs/12.x/migrations)이 있다면, `publishesMigrations` 메서드를 사용하여 해당 디렉터리 또는 파일이 마이그레이션임을 Laravel에 알릴 수 있습니다. Laravel에서 마이그레이션을 퍼블리시할 때 파일 이름의 타임스탬프가 현재 날짜와 시간으로 자동 갱신됩니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishesMigrations([
        __DIR__.'/../database/migrations' => database_path('migrations'),
    ]);
}
```

<a name="language-files"></a>
### 언어 파일 (Language Files)

패키지에 [언어 파일](/docs/12.x/localization)이 있다면, `loadTranslationsFrom` 메서드를 사용하여 Laravel이 이를 어떻게 로드해야 하는지 지정할 수 있습니다. 예를 들어 패키지명이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음을 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지 번역 라인은 `package::file.line` 형식으로 참조할 수 있습니다. 예를 들어, `courier` 패키지의 `messages` 파일에서 `welcome` 라인을 불러오려면 다음과 같이 합니다:

```php
echo trans('courier::messages.welcome');
```

패키지용 JSON 번역 파일을 등록하려면 `loadJsonTranslationsFrom` 메서드를 사용할 수 있습니다. 이 메서드는 패키지의 JSON 번역 파일이 들어있는 디렉터리 경로를 받습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리시하려면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. `publishes` 메서드는 패키지 경로와 퍼블리시 대상 경로의 배열을 받습니다. 예를 들어 `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 Laravel의 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정된 위치로 퍼블리시됩니다.

<a name="views"></a>
### 뷰 (Views)

패키지의 [뷰](/docs/12.x/views)를 Laravel에 등록하려면, 뷰가 있는 위치를 Laravel에 알려주어야 합니다. 이를 위해 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용합니다. `loadViewsFrom`은 뷰 템플릿 경로와 패키지명을 인수로 받습니다. 예를 들어 패키지명이 `courier`이면, `boot` 메서드에 다음과 같이 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 문법으로 참조할 수 있습니다. 따라서 뷰 경로가 등록되면 아래와 같이 `courier` 패키지의 `dashboard` 뷰를 불러올 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이딩

`loadViewsFrom` 메서드를 사용하면, Laravel은 실제로 두 개의 뷰 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 직접 지정한 디렉터리입니다. 즉, `courier` 패키지의 경우, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 경로에 커스텀 뷰를 넣었는지 확인하고, 없으면 지정한 패키지 뷰 디렉터리를 찾습니다. 이를 통해 패키지 사용자는 뷰를 쉽게 커스터마이즈하거나 오버라이드할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰 파일을 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. 이 메서드는 패키지 뷰 경로와 퍼블리시 대상 경로의 배열을 인수로 받습니다:

```php
/**
 * Bootstrap the package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 패키지 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

패키지에서 Blade 컴포넌트를 제공하거나, 컴포넌트를 일반적이지 않은 디렉터리에 둘 경우 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야 합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

컴포넌트가 등록된 후에는 별칭 태그를 사용하여 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로드

또는, `componentNamespace` 메서드를 사용하면 네임스페이스에 따라 컴포넌트 클래스를 자동으로 로드할 수 있습니다. 예를 들어 `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 `Nightshade\Views\Components` 네임스페이스에 있다면 다음과 같이 등록하면 됩니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 벤더 네임스페이스를 사용하여 다음과 같이 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스(Pascal Case)로 변환하여 해당 클래스와 자동으로 연결합니다. "dot" 표기법을 통해 하위 디렉터리도 지원됩니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

패키지에 익명 컴포넌트가 있다면, [loadViewsFrom 메서드](#views)로 지정한 "views" 디렉터리 하위에 반드시 `components` 디렉터리를 만들어 그 안에 넣어야 합니다. 그 다음, 패키지의 뷰 네임스페이스를 접두어로 사용하여 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어

Laravel의 기본 `about` 아티즌 명령어는 애플리케이션의 환경과 설정을 요약해서 보여줍니다. 패키지도 추가 정보를 `AboutCommand` 클래스를 통해 이 명령어의 출력에 추가할 수 있습니다. 일반적으로 이 정보는 패키지 서비스 프로바이더의 `boot` 메서드에서 추가합니다:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}
```

<a name="commands"></a>
## 명령어 (Commands)

패키지의 아티즌 명령어를 Laravel과 함께 등록하려면, `commands` 메서드를 사용합니다. 이 메서드는 명령어 클래스명 배열을 인수로 받습니다. 명령어가 등록되면 [Artisan CLI](/docs/12.x/artisan)를 통해 사용할 수 있습니다:

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}
```

<a name="optimize-commands"></a>
### 최적화 명령어

Laravel의 [optimize 명령어](/docs/12.x/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰를 캐시합니다. 패키지에서도 `optimizes` 메서드를 사용하여, `optimize` 또는 `optimize:clear` 명령어 실행 시 함께 호출될 자체 아티즌 명령어를 등록할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->optimizes(
            optimize: 'package:optimize',
            clear: 'package:clear-optimizations',
        );
    }
}
```

<a name="reload-commands"></a>
### 재로드 명령어

Laravel의 [reload 명령어](/docs/12.x/deployment#reloading-services)는 실행 중인 서비스를 종료하여 시스템 프로세스 모니터가 자동으로 다시 시작할 수 있도록 합니다. 패키지에서 자체적으로 등록해야 할 아티즌 명령어가 있을 경우, `reloads` 메서드를 사용하여 `reload` 명령어 실행 시 호출되도록 할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->reloads('package:reload');
    }
}
```

<a name="public-assets"></a>
## 퍼블릭 에셋 (Public Assets)

패키지에는 JavaScript, CSS, 이미지 등의 에셋이 포함될 수 있습니다. 이런 퍼블릭 에셋을 애플리케이션의 `public` 디렉터리로 퍼블리시하려면, 서비스 프로바이더의 `publishes` 메서드를 사용합니다. 아래 예시는 `public` 에셋 그룹 태그도 추가하여 관련 에셋을 그룹 단위로 쉽게 퍼블리시할 수 있도록 했습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 에셋이 지정된 퍼블리시 위치로 복사됩니다. 보통 패키지 업데이트 시마다 에셋이 덮어써져야 하므로, 사용자는 `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱 (Publishing File Groups)

패키지의 에셋과 리소스를 그룹별로 개별 퍼블리싱하고 싶을 수 있습니다. 예를 들어, 사용자가 설정 파일만 퍼블리시하고 에셋은 퍼블리시하지 않도록 할 수 있습니다. 이를 위해 서비스 프로바이더에서 `publishes` 메서드 호출 시 "태그"를 걸어 그룹별로 정의할 수 있습니다. 아래는 `courier` 패키지에서 `courier-config`와 `courier-migrations`라는 두 퍼블리시 그룹을 정의하는 예시입니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishesMigrations([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

이제 사용자는 아래와 같이 `vendor:publish` 명령어의 태그를 지정하여 그룹별로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```

또는 `--provider` 플래그를 사용하여 패키지 서비스 프로바이더가 정의한 모든 퍼블리시 파일을 한 번에 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
