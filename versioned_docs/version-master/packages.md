# 패키지 개발 (Package Development)

- [소개](#introduction)
    - [파사드에 대한 참고 사항](#a-note-on-facades)
- [패키지 디스커버리](#package-discovery)
- [서비스 프로바이더](#service-providers)
- [리소스](#resources)
    - [설정](#configuration)
    - [라우트](#routes)
    - [마이그레이션](#migrations)
    - [언어 파일](#language-files)
    - [뷰(View)](#views)
    - [뷰 컴포넌트](#view-components)
    - ["About" 아티즌 명령어](#about-artisan-command)
- [명령어](#commands)
    - [최적화 명령어](#optimize-commands)
    - [재시작 명령어](#reload-commands)
- [공개 자산](#public-assets)
- [파일 그룹 퍼블리싱](#publishing-file-groups)

<a name="introduction"></a>
## 소개 (Introduction)

패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)처럼 날짜와 관련된 뛰어난 기능을 제공하는 패키지일 수도 있고, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연관지을 수 있도록 해주는 패키지일 수도 있습니다.

패키지에는 여러 종류가 있습니다. 어떤 패키지는 독립형(stand-alone)으로, 어떠한 PHP 프레임워크에서도 동작할 수 있습니다. Carbon과 Pest가 그 예시입니다. 이런 패키지는 `composer.json` 파일에 추가하여 Laravel에서 바로 사용할 수 있습니다.

반면, 일부 패키지는 오직 Laravel에서 사용하도록 설계되어 있습니다. 이러한 패키지는 라우트, 컨트롤러, 뷰, 설정 등 Laravel 애플리케이션을 향상시키기 위해 특별히 고안된 기능을 포함할 수 있습니다. 이 가이드에서는 주로 Laravel에 특화된 패키지 개발에 대해 다룹니다.

<a name="a-note-on-facades"></a>
### 파사드에 대한 참고 사항

Laravel 애플리케이션을 개발할 때, contracts와 facades 중 무엇을 사용하든 테스트 가능성 측면에서 큰 차이가 없습니다. 그러나 패키지를 개발할 경우, 패키지에서는 Laravel의 모든 테스트 헬퍼를 자유롭게 사용할 수 없습니다. 만약 여러분이 패키지가 일반적인 Laravel 애플리케이션에 설치된 것처럼 테스트를 작성하고 싶다면, [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
## 패키지 디스커버리 (Package Discovery)

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 Laravel이 로드해야 할 서비스 프로바이더 목록이 있습니다. 하지만 사용자가 직접 서비스 프로바이더를 목록에 추가하도록 강제하지 않고도, 패키지의 `composer.json` 파일의 `extra` 섹션에 프로바이더를 정의하여 Laravel이 자동으로 로드하도록 할 수 있습니다. 서비스 프로바이더뿐만 아니라, 등록하고자 하는 [파사드](/docs/master/facades)도 함께 명시할 수 있습니다:

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

이렇게 패키지가 디스커버리에 맞게 설정되면, Laravel은 패키지가 설치되는 즉시 해당 서비스 프로바이더와 파사드를 자동으로 등록하여, 사용자에게 매우 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 디스커버리 비활성화

패키지의 소비자(즉, 일반 사용자)로서, 특정 패키지에 대해 패키지 디스커버리를 비활성화하고 싶다면 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 해당 패키지명을 나열할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

또한, 애플리케이션의 `dont-discover` 지시어에 `*` 문자를 사용하여 모든 패키지에 대한 패키지 디스커버리를 비활성화할 수 있습니다:

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

[서비스 프로바이더](/docs/master/providers)는 패키지와 Laravel을 연결하는 지점입니다. 서비스 프로바이더는 Laravel의 [서비스 컨테이너](/docs/master/container)에 각종 객체나 기능을 바인딩하고, 뷰, 설정, 언어 파일과 같은 패키지 리소스가 어디에 있는지 Laravel이 알 수 있도록 해 줍니다.

서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속하며, `register` 및 `boot` 두 가지 메서드를 가집니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으므로, 여러분의 패키지의 의존 패키지로 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶다면 [관련 문서](/docs/master/providers)를 참고하시기 바랍니다.

<a name="resources"></a>
## 리소스 (Resources)

<a name="configuration"></a>
### 설정 (Configuration)

일반적으로 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리에 퍼블리시해야 합니다. 이렇게 하면 사용자가 패키지의 기본 설정을 손쉽게 재정의할 수 있습니다. 설정 파일을 퍼블리시할 수 있도록 하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

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

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정된 경로로 복사됩니다. 퍼블리시된 설정 파일의 값은 다른 설정 파일과 마찬가지로 접근할 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일 내에서는 클로저를 정의해서는 안 됩니다. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 올바르게 직렬화되지 않을 수 있습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 설정

패키지의 기본 설정 파일과 애플리케이션에 퍼블리시된 복사본을 병합(merge)할 수도 있습니다. 이렇게 하면, 사용자는 오버라이드가 필요한 옵션만 부분적으로 정의할 수 있습니다. 설정 파일의 값을 병합하려면, 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하세요.

`mergeConfigFrom` 메서드의 첫 번째 인자는 패키지 설정 파일의 경로이고, 두 번째 인자는 애플리케이션 설정 파일의 이름입니다:

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
> 이 메서드는 설정 배열의 최상위 레벨만 병합합니다. 사용자가 다차원 설정 배열을 일부만 지정할 경우, 없는 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트 (Routes)

패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드를 이용해 로드할 수 있습니다. 이 메서드는 애플리케이션의 라우트가 이미 캐싱되어 있는지 자동으로 판단하고, 만약 라우트가 캐싱되어 있다면 해당 파일을 불러오지 않습니다:

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

패키지에 [데이터베이스 마이그레이션](/docs/master/migrations)이 포함되어 있다면, `publishesMigrations` 메서드를 사용하여 해당 디렉터리나 파일에 마이그레이션이 있음을 Laravel에 알릴 수 있습니다. Laravel이 마이그레이션 파일을 퍼블리싱할 때, 파일 이름의 타임스탬프는 현재 날짜와 시간으로 자동 변경됩니다:

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

패키지에 [언어 파일](/docs/master/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드를 이용해 Laravel에 파일을 불러오는 방법을 지정할 수 있습니다. 예를 들어, 패키지 이름이 `courier`라면 서비스 프로바이더의 `boot` 메서드에 다음과 같이 추가하세요:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

패키지의 번역 구문은 `package::file.line` 형식의 규칙을 따릅니다. 따라서, `courier` 패키지의 `messages` 파일에 있는 `welcome` 줄을 다음과 같이 로드할 수 있습니다:

```php
echo trans('courier::messages.welcome');
```

패키지의 JSON 번역 파일을 등록하려면, `loadJsonTranslationsFrom` 메서드를 사용할 수 있습니다. 이 메서드는 패키지의 JSON 번역 파일이 들어있는 디렉터리 경로를 인자로 받습니다:

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

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉터리로 퍼블리싱하려면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 메서드는 패키지 경로와 원하는 퍼블리시 위치의 배열을 받습니다. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 합니다:

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

이제 패키지 사용자가 Laravel의 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정한 경로로 퍼블리시 됩니다.

<a name="views"></a>
### 뷰(View) (Views)

패키지의 [뷰](/docs/master/views)를 Laravel에 등록하려면, 뷰가 어디에 위치하는지 Laravel에 알려주어야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용하면 됩니다. 이 메서드는 뷰 템플릿의 경로와 패키지 이름, 두 가지 인자를 받습니다. 예를 들어, 패키지 이름이 `courier`인 경우 서비스 프로바이더의 `boot` 메서드에 다음과 같이 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

패키지 뷰는 `package::view` 규칙에 따라 참조할 수 있습니다. 따라서 서비스 프로바이더에 뷰 경로가 등록된 후에는 다음과 같이 `courier` 패키지의 `dashboard` 뷰를 로드할 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
#### 패키지 뷰 오버라이드

`loadViewsFrom` 메서드를 사용하면, Laravel은 실제로 두 개의 뷰 경로를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와, 지정한 패키지 뷰 경로입니다. 즉, `courier` 패키지를 예로 들면, 개발자가 `resources/views/vendor/courier` 디렉터리에 커스텀 뷰를 작성했는지 먼저 찾고, 없으면 `loadViewsFrom`에서 지정한 패키지 뷰 디렉터리를 참조합니다. 이렇게 하면 패키지 사용자들이 뷰를 손쉽게 커스텀/오버라이드할 수 있습니다.

<a name="publishing-views"></a>
#### 뷰 퍼블리싱

패키지의 뷰 파일을 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리싱하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 이 메서드는 퍼블리시할 패키지 뷰 경로와 원하는 위치의 배열을 인자로 받습니다:

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

이제 패키지 사용자가 Laravel의 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 뷰 파일이 지정한 경로로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트 (View Components)

패키지에서 Blade 컴포넌트를 사용하거나 비표준 디렉터리에 컴포넌트를 위치시킨 경우, 컴포넌트 클래스와 HTML 태그 별칭을 명시적으로 등록해야 합니다. 이를 통해 Laravel이 해당 컴포넌트를 어디서 찾아야 할지 인식할 수 있게 합니다. 보통 패키지의 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다:

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

컴포넌트를 등록하면, 태그 별칭으로 Blade에서 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### 패키지 컴포넌트 자동 로딩

또는, `componentNamespace` 메서드를 사용해 관례(convention)에 따라 컴포넌트 클래스를 자동으로 등록할 수 있습니다. 예를 들어 `Nightshade` 패키지에 `Nightshade\Views\Components` 네임스페이스 아래 `Calendar`, `ColorPicker` 컴포넌트가 있다면 다음과 같이 등록할 수 있습니다:

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

이제 package components를 `package-name::` 문법으로 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름에 파스칼 케이스를 적용하여 자동으로 해당 클래스를 찾아줍니다. 하위 디렉터리도 "dot" 표기법으로 지원됩니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트 (Anonymous Components)

패키지에 익명 컴포넌트가 포함되어 있다면, 반드시 패키지의 "views" 디렉터리 하위에 `components` 디렉터리 안에 위치시켜야 합니다(이 디렉터리는 [loadViewsFrom 메서드](#views)에서 지정한 경로임). 컴포넌트 이름 앞에 패키지 뷰 네임스페이스를 붙여 렌더링하면 됩니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### "About" 아티즌 명령어 ("About" Artisan Command)

Laravel의 기본 제공 `about` 아티즌 명령어는 애플리케이션의 환경 및 설정 요약을 제공합니다. 패키지는 `AboutCommand` 클래스를 통해 이 명령어의 출력에 추가 정보를 표시할 수 있습니다. 일반적으로, 이 정보는 패키지 서비스 프로바이더의 `boot` 메서드에서 추가됩니다:

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

패키지의 아티즌 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 클래스명 배열을 인자로 받습니다. 명령어가 등록되면, [Artisan CLI](/docs/master/artisan)를 사용해 실행할 수 있습니다:

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
### 최적화 명령어 (Optimize Commands)

Laravel의 [optimize 명령어](/docs/master/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰를 캐시합니다. `optimizes` 메서드를 사용하면, 패키지의 아티즌 명령어를 등록하여 `optimize`와 `optimize:clear` 명령이 실행될 때 함께 실행되도록 지정할 수 있습니다:

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
### 재시작 명령어 (Reload Commands)

Laravel의 [reload 명령어](/docs/master/deployment#reloading-services)는 실행 중인 서비스를 종료하여 시스템 프로세스 모니터에 의해 자동 재시작될 수 있도록 합니다. `reloads` 메서드를 사용하면, 패키지의 별도 아티즌 명령어를 등록하여 `reload` 명령이 실행될 때 함께 동작하도록 할 수 있습니다:

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
## 공개 자산 (Public Assets)

패키지에는 JavaScript, CSS, 이미지 등 공개 자산이 포함될 수 있습니다. 이러한 자산을 애플리케이션의 `public` 디렉터리로 퍼블리시하려면 서비스 프로바이더의 `publishes` 메서드를 사용하세요. 예시에서는 `public` 자산 그룹 태그도 함께 추가하여 관련된 자산 묶음을 쉽게 퍼블리시할 수 있도록 합니다:

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

이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 자산이 지정한 위치로 복사됩니다. 패키지 업데이트 시마다 자산을 덮어써야 하므로, 사용자는 `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## 파일 그룹 퍼블리싱 (Publishing File Groups)

패키지의 자산이나 리소스를 별도의 그룹으로 나누어 퍼블리싱할 수도 있습니다. 예를 들어, 사용자가 패키지의 설정 파일만 퍼블리시하거나, 자산만 별도로 퍼블리시할 수 있도록 할 수 있습니다. 이는 서비스 프로바이더의 `publishes` 메서드를 호출할 때 "태그(tag)"를 부여하여 처리합니다. 예를 들어, `courier` 패키지에서 `courier-config`와 `courier-migrations`라는 두 개의 퍼블리시 그룹을 정의하는 방법은 다음과 같습니다:

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

사용자는 `vendor:publish` 명령어에서 태그를 지정하여 각 그룹을 독립적으로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```

또한, `--provider` 플래그를 사용하여 서비스 프로바이더가 정의한 모든 퍼블리시 가능한 파일을 한 번에 퍼블리시할 수도 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```