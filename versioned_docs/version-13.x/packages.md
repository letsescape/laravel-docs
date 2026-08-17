<!-- # Package Development -->
# Package Development

- [Introduction](#introduction)
    - [Creating a Package](#creating-a-package)
    - [A Note on Facades](#a-note-on-facades)
- [Package Discovery](#package-discovery)
- [Service Providers](#service-providers)
- [Resources](#resources)
    - [Configuration](#configuration)
    - [Routes](#routes)
    - [Migrations](#migrations)
    - [Language Files](#language-files)
    - [Views](#views)
    - [View Components](#view-components)
    - ["About" Artisan Command](#about-artisan-command)
- [Commands](#commands)
    - [Optimize Commands](#optimize-commands)
    - [Reload Commands](#reload-commands)
- [Public Assets](#public-assets)
- [Publishing File Groups](#publishing-file-groups)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon) or a package that allows you to associate files with Eloquent models like Spatie's [Laravel Media Library](https://github.com/spatie/laravel-medialibrary). -->
패키지는 Laravel에 기능을 추가하는 주요 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)처럼 날짜를 다루기 위한 훌륭한 방법일 수도 있고, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 연동할 수 있도록 해주는 패키지일 수도 있습니다.

<!-- There are different types of packages. Some packages are stand-alone, meaning they work with any PHP framework. Carbon and Pest are examples of stand-alone packages. Any of these packages may be used with Laravel by requiring them in your `composer.json` file. -->
패키지에는 여러 종류가 있습니다. 어떤 패키지는 독립 실행형(stand-alone)으로, 모든 PHP 프레임워크에서 동작할 수 있습니다. Carbon과 Pest가 그 예시입니다. 이런 패키지들도 `composer.json` 파일에 require하여 Laravel에서 사용할 수 있습니다.

<!-- On the other hand, other packages are specifically intended for use with Laravel. These packages may have routes, controllers, views, and configuration specifically intended to enhance a Laravel application. This guide primarily covers the development of those packages that are Laravel specific. -->
반대로, 일부 패키지는 오직 Laravel에서 사용하기 위한 목적으로 만들어집니다. 이런 패키지에는 Laravel 애플리케이션을 확장하는 데 적합한 라우트, 컨트롤러, 뷰, 설정 등이 포함돼 있을 수 있습니다. 이 가이드는 주로 Laravel에 특화된 패키지를 개발하는 방법을 다룹니다.

<a name="creating-a-package"></a>
<!-- ### Creating a Package -->
### Creating a Package

<!-- The easiest way to start building a new Laravel package is the official [Laravel package skeleton](https://github.com/laravel/package-skeleton). The skeleton provides everything you need to build a Laravel package, including a service provider, testing via Pest, static analysis via Larastan, code formatting via Pint, and a workbench application for end-to-end package development. You can create a new package using the `package` command of the [Laravel installer CLI](/docs/13.x/installation#creating-a-laravel-project): -->
새로운 Laravel 패키지 개발을 시작하는 가장 쉬운 방법은 공식 [Laravel package skeleton](https://github.com/laravel/package-skeleton)을 사용하는 것입니다. 이 스켈레톤에는 서비스 프로바이더, Pest를 사용한 테스트, Larastan을 사용한 정적 분석, Pint를 사용한 코드 포맷팅, 엔드 투 엔드 패키지 개발을 위한 워크벤치 애플리케이션 등 Laravel 패키지를 만드는 데 필요한 모든 것이 포함되어 있습니다. [Laravel installer CLI](/docs/13.x/installation#creating-a-laravel-project)의 `package` 명령어를 사용해 새 패키지를 만들 수 있습니다.

```shell
laravel package my-package
```

<!-- An interactive configuration script will personalize the skeleton for your package, setting up your namespace, service provider, and only the features you need, such as configuration files, routes, views, translations, migrations, assets, commands, and a facade. -->
대화형 설정 스크립트가 패키지에 맞게 스켈레톤을 구성하고, 네임스페이스와 서비스 프로바이더를 설정하며, 설정 파일, 라우트, 뷰, 번역, 마이그레이션, 에셋, 명령어, 파사드 등 필요한 기능만 추가합니다.

<a name="a-note-on-facades"></a>
<!-- ### A Note on Facades -->
### A Note on Facades

<!-- When writing a Laravel application, it generally does not matter if you use contracts or facades since both provide essentially equal levels of testability. However, when writing packages, your package will not typically have access to all of Laravel's testing helpers. If you would like to be able to write your package tests as if the package were installed inside a typical Laravel application, you may use the [Orchestral Testbench](https://github.com/orchestral/testbench) package. -->
Laravel 애플리케이션을 개발할 때는 contracts나 facades 모두 테스트 가능성 측면에서 거의 동일하므로 어느 것을 사용해도 큰 문제가 되지 않습니다. 그러나 패키지를 개발할 때는 Laravel의 모든 테스트 헬퍼를 사용할 수 없는 경우가 많습니다. 패키지의 테스트를 일반적인 Laravel 애플리케이션 안에 설치된 것처럼 작성하려면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다.

<a name="package-discovery"></a>
<!-- ## Package Discovery -->
## Package Discovery

<!-- A Laravel application's `bootstrap/providers.php` file contains the list of service providers that should be loaded by Laravel. However, instead of requiring users to manually add your service provider to the list, you may define the provider in the `extra` section of your package's `composer.json` file so that it is automatically loaded by Laravel. In addition to service providers, you may also list any [facades](/docs/13.x/facades) you would like to be registered: -->
Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 Laravel에서 로드해야 하는 서비스 프로바이더 목록이 들어 있습니다. 하지만 사용자에게 서비스 프로바이더를 직접 목록에 추가하도록 요구하지 않고, 패키지의 `composer.json` 파일 `extra` 섹션에 프로바이더를 정의해두면 Laravel이 자동으로 이를 로드하도록 할 수 있습니다. 서비스 프로바이더 뿐 아니라 등록하고 싶은 [facades](/docs/13.x/facades)도 함께 지정할 수 있습니다:

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

<!-- Once your package has been configured for discovery, Laravel will automatically register its service providers and facades when it is installed, creating a convenient installation experience for your package's users. -->
패키지가 자동 발견에 맞게 구성된 경우, Laravel은 패키지가 설치되는 즉시 서비스 프로바이더와 파사드를 자동으로 등록하여 사용자에게 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
<!-- #### Opting Out of Package Discovery -->
#### Opting Out of Package Discovery

<!-- If you are the consumer of a package and would like to disable package discovery for a package, you may list the package name in the `extra` section of your application's `composer.json` file: -->
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

<!-- You may disable package discovery for all packages using the `*` character inside of your application's `dont-discover` directive: -->
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
<!-- ## Service Providers -->
## Service Providers

<!-- [Service providers](/docs/13.x/providers) are the connection point between your package and Laravel. A service provider is responsible for binding things into Laravel's [service container](/docs/13.x/container) and informing Laravel where to load package resources such as views, configuration, and language files. -->
[Service providers](/docs/13.x/providers)는 패키지와 Laravel을 연결해주는 중개자 역할을 합니다. 서비스 프로바이더는 Laravel의 [service container](/docs/13.x/container)에 다양한 객체를 바인딩하고, 패키지의 뷰, 설정, 언어 파일 등 리소스의 위치를 Laravel에 알려주는 책임을 집니다.

<!-- A service provider extends the `Illuminate\Support\ServiceProvider` class and contains two methods: `register` and `boot`. The base `ServiceProvider` class is located in the `illuminate/support` Composer package, which you should add to your own package's dependencies. To learn more about the structure and purpose of service providers, check out [their documentation](/docs/13.x/providers). -->
서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장하며, `register`와 `boot`라는 두 가지 메서드를 가집니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으므로, 이를 패키지 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 자세히 알고 싶다면 [their documentation](/docs/13.x/providers)를 참고하세요.

<a name="resources"></a>
<!-- ## Resources -->
## Resources

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Typically, you will need to publish your package's configuration file to the application's `config` directory. This will allow users of your package to easily override your default configuration options. To allow your configuration files to be published, call the `publishes` method from the `boot` method of your service provider: -->
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

<!-- Now, when users of your package execute Laravel's `vendor:publish` command, your file will be copied to the specified publish location. Once your configuration has been published, its values may be accessed like any other configuration file: -->
이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면 설정 파일이 지정된 위치에 복사됩니다. 설정 파일이 퍼블리시된 후에는 일반 설정 파일처럼 값을 읽을 수 있습니다:

```php
$value = config('courier.option');
```

> [!WARNING]
> 설정 파일 내에 클로저를 정의하지 마세요. 사용자가 `config:cache` 아티즌 명령어를 실행할 때 올바르게 직렬화되지 않습니다.

<a name="default-package-configuration"></a>
<!-- #### Default Package Configuration -->
#### Default Package Configuration

<!-- You may also merge your own package configuration file with the application's published copy. This will allow your users to define only the options they actually want to override in the published copy of the configuration file. To merge the configuration file values, use the `mergeConfigFrom` method within your service provider's `register` method. -->
패키지의 설정 파일을 애플리케이션에 퍼블리시된 복사본과 병합(merge)할 수도 있습니다. 이렇게 하면 사용자는 오버라이드하고 싶은 옵션만 설정 파일에 정의해 두면 됩니다. 설정 값 병합은 서비스 프로바이더의 `register` 메서드에서 `mergeConfigFrom` 메서드를 사용하면 됩니다.

<!-- The `mergeConfigFrom` method accepts the path to your package's configuration file as its first argument and the name of the application's copy of the configuration file as its second argument: -->
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
<!-- ### Routes -->
### Routes

<!-- If your package contains routes, you may load them using the `loadRoutesFrom` method. This method will automatically determine if the application's routes are cached and will not load your routes file if the routes have already been cached: -->
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
<!-- ### Migrations -->
### Migrations

<!-- If your package contains [database migrations](/docs/13.x/migrations), you may use the `publishesMigrations` method to inform Laravel that the given directory or file contains migrations. When Laravel publishes the migrations, it will automatically update the timestamp within their filename to reflect the current date and time: -->
패키지에 [database migrations](/docs/13.x/migrations)이 있다면, `publishesMigrations` 메서드를 사용하여 해당 디렉터리 또는 파일이 마이그레이션임을 Laravel에 알릴 수 있습니다. Laravel에서 마이그레이션을 퍼블리시할 때 파일 이름의 타임스탬프가 현재 날짜와 시간으로 자동 갱신됩니다:

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
<!-- ### Language Files -->
### Language Files

<!-- If your package contains [language files](/docs/13.x/localization), you may use the `loadTranslationsFrom` method to inform Laravel how to load them. For example, if your package is named `courier`, you should add the following to your service provider's `boot` method: -->
패키지에 [language files](/docs/13.x/localization)이 있다면, `loadTranslationsFrom` 메서드를 사용하여 Laravel이 이를 어떻게 로드해야 하는지 지정할 수 있습니다. 예를 들어 패키지명이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 다음을 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}
```

<!-- Package translation lines are referenced using the `package::file.line` syntax convention. So, you may load the `courier` package's `welcome` line from the `messages` file like so: -->
패키지 번역 라인은 `package::file.line` 형식으로 참조할 수 있습니다. 예를 들어, `courier` 패키지의 `messages` 파일에서 `welcome` 라인을 불러오려면 다음과 같이 합니다:

```php
echo trans('courier::messages.welcome');
```

<!-- You can register JSON translation files for your package using the `loadJsonTranslationsFrom` method. This method accepts the path to the directory that contains your package's JSON translation files: -->
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
<!-- #### Publishing Language Files -->
#### Publishing Language Files

<!-- If you would like to publish your package's language files to the application's `lang/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package paths and their desired publish locations. For example, to publish the language files for the `courier` package, you may do the following: -->
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

<!-- Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's language files will be published to the specified publish location. -->
이제 패키지 사용자가 Laravel의 `vendor:publish` 아티즌 명령어를 실행하면, 패키지의 언어 파일이 지정된 위치로 퍼블리시됩니다.

<a name="views"></a>
<!-- ### Views -->
### Views

<!-- To register your package's [views](/docs/13.x/views) with Laravel, you need to tell Laravel where the views are located. You may do this using the service provider's `loadViewsFrom` method. The `loadViewsFrom` method accepts two arguments: the path to your view templates and your package's name. For example, if your package's name is `courier`, you would add the following to your service provider's `boot` method: -->
패키지의 [views](/docs/13.x/views)를 Laravel에 등록하려면, 뷰가 있는 위치를 Laravel에 알려주어야 합니다. 이를 위해 서비스 프로바이더의 `loadViewsFrom` 메서드를 사용합니다. `loadViewsFrom`은 뷰 템플릿 경로와 패키지명을 인수로 받습니다. 예를 들어 패키지명이 `courier`이면, `boot` 메서드에 다음과 같이 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

<!-- Package views are referenced using the `package::view` syntax convention. So, once your view path is registered in a service provider, you may load the `dashboard` view from the `courier` package like so: -->
패키지 뷰는 `package::view` 문법으로 참조할 수 있습니다. 따라서 뷰 경로가 등록되면 아래와 같이 `courier` 패키지의 `dashboard` 뷰를 불러올 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
<!-- #### Overriding Package Views -->
#### Overriding Package Views

<!-- When you use the `loadViewsFrom` method, Laravel actually registers two locations for your views: the application's `resources/views/vendor` directory and the directory you specify. So, using the `courier` package as an example, Laravel will first check if a custom version of the view has been placed in the `resources/views/vendor/courier` directory by the developer. Then, if the view has not been customized, Laravel will search the package view directory you specified in your call to `loadViewsFrom`. This makes it easy for package users to customize / override your package's views. -->
`loadViewsFrom` 메서드를 사용하면, Laravel은 실제로 두 개의 뷰 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 직접 지정한 디렉터리입니다. 즉, `courier` 패키지의 경우, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 경로에 커스텀 뷰를 넣었는지 확인하고, 없으면 `loadViewsFrom` 호출에서 지정한 패키지 뷰 디렉터리를 찾습니다. 이를 통해 패키지 사용자는 뷰를 쉽게 사용자 지정하거나 오버라이드할 수 있습니다.

<a name="publishing-views"></a>
<!-- #### Publishing Views -->
#### Publishing Views

<!-- If you would like to make your views available for publishing to the application's `resources/views/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package view paths and their desired publish locations: -->
패키지의 뷰 파일을 애플리케이션의 `resources/views/vendor` 디렉터리로 퍼블리시하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용할 수 있습니다. `publishes` 메서드는 패키지 뷰 경로와 퍼블리시 대상 경로의 배열을 인수로 받습니다:

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

<!-- Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's views will be copied to the specified publish location. -->
이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 패키지 뷰가 지정된 위치로 복사됩니다.

<a name="view-components"></a>
<!-- ### View Components -->
### View Components

<!-- If you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider: -->
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

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
컴포넌트가 등록된 후에는 별칭 태그를 사용하여 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
<!-- #### Autoloading Package Components -->
#### Autoloading Package Components

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Nightshade\Views\Components` namespace: -->
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

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
이렇게 하면 `package-name::` 구문을 사용하여 벤더 네임스페이스로 패키지 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 케이스(Pascal Case)로 변환하여 해당 클래스와 자동으로 연결합니다. "dot" 표기법을 통해 하위 디렉터리도 지원됩니다.

<a name="anonymous-components"></a>
<!-- #### Anonymous Components -->
#### Anonymous Components

<!-- If your package contains anonymous components, they must be placed within a `components` directory of your package's "views" directory (as specified by the [loadViewsFrom method](#views)). Then, you may render them by prefixing the component name with the package's view namespace: -->
패키지에 익명 컴포넌트가 있다면, [loadViewsFrom method](#views)로 지정한 "views" 디렉터리 하위에 반드시 `components` 디렉터리를 만들어 그 안에 넣어야 합니다. 그 다음, 패키지의 뷰 네임스페이스를 접두어로 사용하여 렌더링할 수 있습니다:

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
<!-- ### "About" Artisan Command -->
### "About" Artisan Command

<!-- Laravel's built-in `about` Artisan command provides a synopsis of the application's environment and configuration. Packages may push additional information to this command's output via the `AboutCommand` class. Typically, this information may be added from your package service provider's `boot` method: -->
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
<!-- ## Commands -->
## Commands

<!-- To register your package's Artisan commands with Laravel, you may use the `commands` method. This method expects an array of command class names. Once the commands have been registered, you may execute them using the [Artisan CLI](/docs/13.x/artisan): -->
패키지의 아티즌 명령어를 Laravel과 함께 등록하려면, `commands` 메서드를 사용합니다. 이 메서드는 명령어 클래스명 배열을 인수로 받습니다. 명령어가 등록되면 [Artisan CLI](/docs/13.x/artisan)를 통해 사용할 수 있습니다:

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
<!-- ### Optimize Commands -->
### Optimize Commands

<!-- Laravel's [optimize command](/docs/13.x/deployment#optimization) caches the application's configuration, events, routes, and views. Using the `optimizes` method, you may register your package's own Artisan commands that should be invoked when the `optimize` and `optimize:clear` commands are executed: -->
Laravel의 [optimize command](/docs/13.x/deployment#optimization)는 애플리케이션의 설정, 이벤트, 라우트, 뷰를 캐시합니다. 패키지에서도 `optimizes` 메서드를 사용하여, `optimize` 또는 `optimize:clear` 명령어 실행 시 함께 호출될 자체 아티즌 명령어를 등록할 수 있습니다:

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
<!-- ### Reload Commands -->
### Reload Commands

<!-- Laravel's [reload command](/docs/13.x/deployment#reloading-services) terminates any running services so they can be automatically restarted by a system process monitor. Using the `reloads` method, you may register your package's own Artisan commands that should be invoked when the `reload` command is executed: -->
Laravel의 [reload command](/docs/13.x/deployment#reloading-services)는 실행 중인 서비스를 종료하여 시스템 프로세스 모니터가 자동으로 다시 시작할 수 있도록 합니다. 패키지에서 자체적으로 등록해야 할 아티즌 명령어가 있을 경우, `reloads` 메서드를 사용하여 `reload` 명령어 실행 시 호출되도록 할 수 있습니다:

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
<!-- ## Public Assets -->
## Public Assets

<!-- Your package may have assets such as JavaScript, CSS, and images. To publish these assets to the application's `public` directory, use the service provider's `publishes` method. In this example, we will also add a `public` asset group tag, which may be used to easily publish groups of related assets: -->
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

<!-- Now, when your package's users execute the `vendor:publish` command, your assets will be copied to the specified publish location. Since users will typically need to overwrite the assets every time the package is updated, they may use the `--force` flag: -->
이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 에셋이 지정된 퍼블리시 위치로 복사됩니다. 보통 패키지 업데이트 시마다 에셋이 덮어써져야 하므로, 사용자는 `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
<!-- ## Publishing File Groups -->
## Publishing File Groups

<!-- You may want to publish groups of package assets and resources separately. For instance, you might want to allow your users to publish your package's configuration files without being forced to publish your package's assets. You may do this by "tagging" them when calling the `publishes` method from a package's service provider. For example, let's use tags to define two publish groups for the `courier` package (`courier-config` and `courier-migrations`) in the `boot` method of the package's service provider: -->
패키지의 에셋과 리소스를 그룹별로 개별 퍼블리싱하고 싶을 수 있습니다. 예를 들어, 사용자가 설정 파일만 퍼블리시하고 에셋은 퍼블리시하지 않도록 할 수 있습니다. 이를 위해 서비스 프로바이더에서 `publishes` 메서드 호출 시 "태그"를 걸어 그룹별로 정의할 수 있습니다. 아래는 패키지 서비스 프로바이더의 `boot` 메서드에서 `courier` 패키지에 `courier-config`와 `courier-migrations`라는 두 퍼블리시 그룹을 정의하는 예시입니다:

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

<!-- Now your users may publish these groups separately by referencing their tag when executing the `vendor:publish` command: -->
이제 사용자는 아래와 같이 `vendor:publish` 명령어의 태그를 지정하여 그룹별로 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config
```

<!-- Your users can also publish all publishable files defined by your package's service provider using the `--provider` flag: -->
또는 `--provider` 플래그를 사용하여 패키지 서비스 프로바이더가 정의한 모든 퍼블리시 파일을 한 번에 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"
```
