<!-- # Package Development -->
# Package Development

- [Introduction](#introduction)
    - [A Note On Facades](#a-note-on-facades)
- [Package Discovery](#package-discovery)
- [Service Providers](#service-providers)
- [Resources](#resources)
    - [Configuration](#configuration)
    - [Migrations](#migrations)
    - [Routes](#routes)
    - [Translations](#translations)
    - [Views](#views)
    - [View Components](#view-components)
- [Commands](#commands)
- [Public Assets](#public-assets)
- [Publishing File Groups](#publishing-file-groups)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon) or a package that allows you to associate files with Eloquent models like Spatie's [Laravel Media Library](https://github.com/spatie/laravel-medialibrary). -->
패키지는 Laravel에 기능을 추가하는 기본적인 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon)과 같이 날짜를 편리하게 다루는 라이브러리일 수도 있고, Spatie의 [Laravel Media Library](https://github.com/spatie/laravel-medialibrary)처럼 Eloquent 모델에 파일을 쉽게 연결할 수 있게 해주는 패키지일 수도 있습니다.

<!-- There are different types of packages. Some packages are stand-alone, meaning they work with any PHP framework. Carbon and PHPUnit are examples of stand-alone packages. Any of these packages may be used with Laravel by requiring them in your `composer.json` file. -->
패키지에는 여러 종류가 있습니다. 일부 패키지는 독립형(stand-alone)으로, 모든 PHP 프레임워크에서 사용할 수 있습니다. Carbon과 PHPUnit이 대표적인 독립형 패키지이며, 이러한 패키지는 `composer.json` 파일에 추가해서 Laravel 프로젝트에서 그대로 사용할 수 있습니다.

<!-- On the other hand, other packages are specifically intended for use with Laravel. These packages may have routes, controllers, views, and configuration specifically intended to enhance a Laravel application. This guide primarily covers the development of those packages that are Laravel specific. -->
반면, Laravel에 특화되어 만들어진 패키지도 있습니다. 이런 패키지는 라우트, 컨트롤러, 뷰, 설정 파일 등을 포함해 Laravel 애플리케이션의 기능을 확장하는 데 집중합니다. 이 가이드에서는 Laravel 전용 패키지 개발 방법을 중심으로 설명합니다.

<a name="a-note-on-facades"></a>
<!-- ### A Note On Facades -->
### A Note On Facades

<!-- When writing a Laravel application, it generally does not matter if you use contracts or facades since both provide essentially equal levels of testability. However, when writing packages, your package will not typically have access to all of Laravel's testing helpers. If you would like to be able to write your package tests as if the package were installed inside a typical Laravel application, you may use the [Orchestral Testbench](https://github.com/orchestral/testbench) package. -->
Laravel 애플리케이션을 작성할 때는 contract나 파사드를 사용하는 것에 큰 차이가 없습니다. 두 방식 모두 테스트 코드 작성에 있어서 거의 동일한 수준의 효율성을 제공합니다. 그러나 패키지를 작성할 때에는 Laravel의 테스트 관련 도우미(헬퍼)에 모두 접근할 수 없을 수도 있습니다. 만약 패키지를 일반적인 Laravel 애플리케이션 안에 설치한 것처럼 테스트하고 싶다면, [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용하면 됩니다.

<a name="package-discovery"></a>
<!-- ## Package Discovery -->
## Package Discovery

<!-- In a Laravel application's `config/app.php` configuration file, the `providers` option defines a list of service providers that should be loaded by Laravel. When someone installs your package, you will typically want your service provider to be included in this list. Instead of requiring users to manually add your service provider to the list, you may define the provider in the `extra` section of your package's `composer.json` file. In addition to service providers, you may also list any [facades](/docs/8.x/facades) you would like to be registered: -->
Laravel 애플리케이션의 `config/app.php` 파일에서 `providers` 옵션은 로딩되어야 할 서비스 프로바이더 목록을 정의합니다. 누군가 여러분의 패키지를 설치하면, 일반적으로 서비스 프로바이더도 이 목록에 포함되길 원할 것입니다. 사용자에게 이 과정을 직접 맡기는 대신, 패키지의 `composer.json` 파일의 `extra` 섹션에 서비스 프로바이더를 정의할 수 있습니다. 서비스 프로바이더 외에도, 등록하고 싶은 [facades](/docs/8.x/facades)가 있다면 aliases 항목에 추가할 수도 있습니다:

```
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
이렇게 패키지에 자동 등록 설정을 해두면, 유저가 패키지를 설치할 때 Laravel이 자동으로 서비스 프로바이더와 파사드를 등록해 줍니다. 덕분에 패키지를 설치하는 과정이 훨씬 간편해집니다.

<a name="opting-out-of-package-discovery"></a>
<!-- ### Opting Out Of Package Discovery -->
### Opting Out Of Package Discovery

<!-- If you are the consumer of a package and would like to disable package discovery for a package, you may list the package name in the `extra` section of your application's `composer.json` file: -->
패키지 사용자가 패키지 자동 등록(package discovery)을 비활성화하고 싶을 때는, 애플리케이션의 `composer.json` 파일 `extra` 섹션에 해당 패키지명을 나열하면 됩니다:

```
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

<!-- You may disable package discovery for all packages using the `*` character inside of your application's `dont-discover` directive: -->
모든 패키지의 자동 등록을 비활성화 하고 싶다면, `dont-discover` 지시어에 `*`를 추가하세요:

```
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

<!-- [Service providers](/docs/8.x/providers) are the connection point between your package and Laravel. A service provider is responsible for binding things into Laravel's [service container](/docs/8.x/container) and informing Laravel where to load package resources such as views, configuration, and localization files. -->
[Service providers](/docs/8.x/providers)는 패키지와 Laravel을 연결하는 지점입니다. 서비스 프로바이더는 Laravel의 [service container](/docs/8.x/container)에 다양한 기능을 바인딩하고, 설정 파일, 뷰, 번역 파일 등 패키지 리소스가 어디에 있는지 Laravel에 알려주는 역할을 합니다.

<!-- A service provider extends the `Illuminate\Support\ServiceProvider` class and contains two methods: `register` and `boot`. The base `ServiceProvider` class is located in the `illuminate/support` Composer package, which you should add to your own package's dependencies. To learn more about the structure and purpose of service providers, check out [their documentation](/docs/8.x/providers). -->
서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장(extends)하며 `register`와 `boot` 두 가지 메서드를 가집니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 포함되어 있으므로, 패키지의 의존성에 추가해야 합니다. 서비스 프로바이더의 구조와 목적에 대해 더 알고 싶다면 [their documentation](/docs/8.x/providers)를 참고하세요.

<a name="resources"></a>
<!-- ## Resources -->
## Resources

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Typically, you will need to publish your package's configuration file to the application's `config` directory. This will allow users of your package to easily override your default configuration options. To allow your configuration files to be published, call the `publishes` method from the `boot` method of your service provider: -->
일반적으로, 패키지의 설정 파일을 애플리케이션의 `config` 디렉터리로 복사해서 배포해야 합니다. 이를 통해 패키지 사용자는 기본 설정 값을 쉽게 재정의할 수 있습니다. 설정 파일 배포를 지원하려면, 서비스 프로바이더의 `boot` 메서드에서 `publishes` 메서드를 호출하세요:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

<!-- Now, when users of your package execute Laravel's `vendor:publish` command, your file will be copied to the specified publish location. Once your configuration has been published, its values may be accessed like any other configuration file: -->
이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 설정 파일이 지정한 위치로 복사됩니다. 설정 파일이 복사된 후에는 다른 설정 파일과 동일하게 값을 불러올 수 있습니다:

```
$value = config('courier.option');
```

> [!NOTE]
> 설정 파일에서 클로저(익명 함수)는 정의하지 않아야 합니다. `config:cache` 아티즌 명령어를 실행할 때 직렬화가 올바르게 동작하지 않기 때문입니다.

<a name="default-package-configuration"></a>
<!-- #### Default Package Configuration -->
#### Default Package Configuration

<!-- You may also merge your own package configuration file with the application's published copy. This will allow your users to define only the options they actually want to override in the published copy of the configuration file. To merge the configuration file values, use the `mergeConfigFrom` method within your service provider's `register` method. -->
패키지의 설정 파일을 애플리케이션에 배포한 복사본과 병합할 수도 있습니다. 이를 통해 사용자는 변경하고 싶은 옵션만 설정 파일에서 오버라이드(재정의)할 수 있습니다. 설정 파일의 값을 병합하려면, 서비스 프로바이더의 `register` 메서드 안에서 `mergeConfigFrom` 메서드를 사용하세요.

<!-- The `mergeConfigFrom` method accepts the path to your package's configuration file as its first argument and the name of the application's copy of the configuration file as its second argument: -->
`mergeConfigFrom` 메서드의 첫 번째 인자는 패키지의 설정 파일 경로, 두 번째 인자는 애플리케이션에 복사될 설정 파일의 이름입니다:

```
/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!NOTE]
> 이 메서드는 설정 배열의 1단계만 병합합니다. 사용자가 여러 단계로 구성된 설정 배열을 일부만 정의한 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
<!-- ### Routes -->
### Routes

<!-- If your package contains routes, you may load them using the `loadRoutesFrom` method. This method will automatically determine if the application's routes are cached and will not load your routes file if the routes have already been cached: -->
패키지에 라우트가 포함되어 있다면, `loadRoutesFrom` 메서드로 라우트를 불러올 수 있습니다. 이 메서드는 애플리케이션의 라우트가 캐시되어 있으면 자동으로 추가 라우트를 불러오지 않습니다:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
<!-- ### Migrations -->
### Migrations

<!-- If your package contains [database migrations](/docs/8.x/migrations), you may use the `loadMigrationsFrom` method to inform Laravel how to load them. The `loadMigrationsFrom` method accepts the path to your package's migrations as its only argument: -->
패키지에 [database migrations](/docs/8.x/migrations)이 포함되어 있다면, `loadMigrationsFrom` 메서드로 Laravel에 알려줄 수 있습니다. `loadMigrationsFrom` 메서드는 패키지의 마이그레이션 디렉터리 경로만 인자로 받습니다:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
}
```

<!-- Once your package's migrations have been registered, they will automatically be run when the `php artisan migrate` command is executed. You do not need to export them to the application's `database/migrations` directory. -->
이제 패키지의 마이그레이션이 등록되어, 사용자가 `php artisan migrate` 명령어를 실행하면 자동으로 적용됩니다. 별도로 애플리케이션의 `database/migrations` 디렉터리로 복사할 필요가 없습니다.

<a name="translations"></a>
<!-- ### Translations -->
### Translations

<!-- If your package contains [translation files](/docs/8.x/localization), you may use the `loadTranslationsFrom` method to inform Laravel how to load them. For example, if your package is named `courier`, you should add the following to your service provider's `boot` method: -->
패키지에 [translation files](/docs/8.x/localization)이 포함되어 있다면, `loadTranslationsFrom` 메서드로 Laravel에 경로를 등록할 수 있습니다. 예를 들어, 패키지 이름이 `courier`라면, 서비스 프로바이더의 `boot` 메서드에 아래와 같이 추가합니다:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');
}
```

<!-- Package translations are referenced using the `package::file.line` syntax convention. So, you may load the `courier` package's `welcome` line from the `messages` file like so: -->
패키지 번역은 `package::file.line` 문법을 사용해 참조하게 됩니다. 예를 들어 `courier` 패키지의 `messages` 파일 내 `welcome` 문구를 불러오려면 다음과 같이 사용할 수 있습니다:

```
echo trans('courier::messages.welcome');
```

<a name="publishing-translations"></a>
<!-- #### Publishing Translations -->
#### Publishing Translations

<!-- If you would like to publish your package's translations to the application's `resources/lang/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package paths and their desired publish locations. For example, to publish the translation files for the `courier` package, you may do the following: -->
패키지의 번역 파일을 애플리케이션의 `resources/lang/vendor` 디렉터리로 복사해서 배포하고 싶다면, 서비스 프로바이더의 `publishes` 메서드를 사용합니다. `publishes` 메서드는 패키지 경로와 배포할 위치의 배열을 인자로 받습니다. 예를 들어 `courier` 패키지의 번역 파일을 배포하려면 다음과 같이 합니다:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');

    $this->publishes([
        __DIR__.'/../resources/lang' => resource_path('lang/vendor/courier'),
    ]);
}
```

<!-- Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's translations will be published to the specified publish location. -->
이제 패키지 사용자가 Laravel의 `vendor:publish` 아티즌 명령어를 실행하면, 번역 파일이 지정한 위치로 복사됩니다.

<a name="views"></a>
<!-- ### Views -->
### Views

<!-- To register your package's [views](/docs/8.x/views) with Laravel, you need to tell Laravel where the views are located. You may do this using the service provider's `loadViewsFrom` method. The `loadViewsFrom` method accepts two arguments: the path to your view templates and your package's name. For example, if your package's name is `courier`, you would add the following to your service provider's `boot` method: -->
패키지의 [views](/docs/8.x/views)를 Laravel에서 사용할 수 있도록 등록하려면, 뷰 파일이 어디에 있는지 Laravel에 알려야 합니다. 서비스 프로바이더의 `loadViewsFrom` 메서드를 이용합니다. `loadViewsFrom` 메서드는 뷰 템플릿 경로와 패키지 이름을 인자로 받습니다. 예를 들어, 패키지명이 `courier`라면 `boot` 메서드에 아래 코드를 추가하세요:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

<!-- Package views are referenced using the `package::view` syntax convention. So, once your view path is registered in a service provider, you may load the `dashboard` view from the `courier` package like so: -->
패키지 뷰는 `package::view` 문법으로 참조합니다. 뷰 경로를 등록한 후에는 아래와 같이 `courier` 패키지의 `dashboard` 뷰를 사용할 수 있습니다:

```
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
<!-- #### Overriding Package Views -->
#### Overriding Package Views

<!-- When you use the `loadViewsFrom` method, Laravel actually registers two locations for your views: the application's `resources/views/vendor` directory and the directory you specify. So, using the `courier` package as an example, Laravel will first check if a custom version of the view has been placed in the `resources/views/vendor/courier` directory by the developer. Then, if the view has not been customized, Laravel will search the package view directory you specified in your call to `loadViewsFrom`. This makes it easy for package users to customize / override your package's views. -->
`loadViewsFrom` 메서드를 사용하면, Laravel은 내부적으로 두 곳을 뷰 탐색 경로로 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 패키지 뷰 디렉터리입니다. 예를 들어, `courier` 패키지의 경우 개발자가 `resources/views/vendor/courier` 디렉터리에 뷰 파일을 직접 만들어 두었다면, Laravel은 이 파일부터 우선적으로 불러옵니다. 해당 뷰 파일이 없으면 `loadViewsFrom` 호출에서 지정한 패키지 내부 뷰 디렉터리에서 찾게 됩니다. 이를 통해 패키지 사용자가 뷰를 쉽게 커스터마이즈/오버라이드할 수 있습니다.

<a name="publishing-views"></a>
<!-- #### Publishing Views -->
#### Publishing Views

<!-- If you would like to make your views available for publishing to the application's `resources/views/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package view paths and their desired publish locations: -->
패키지의 뷰 파일을 애플리케이션의 `resources/views/vendor` 디렉터리로 배포하려면, 서비스 프로바이더의 `publishes` 메서드를 사용합니다. `publishes` 메서드는 패키지 뷰 경로와 복사할 위치의 경로 배열을 받습니다:

```
/**
 * Bootstrap the package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

<!-- Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's views will be copied to the specified publish location. -->
이제 패키지 사용자가 Laravel의 `vendor:publish` 명령어를 실행하면, 뷰 파일이 지정한 위치로 복사됩니다.

<a name="view-components"></a>
<!-- ### View Components -->
### View Components

<!-- If your package contains [view components](/docs/8.x/blade#components), you may use the `loadViewComponentsAs` method to inform Laravel how to load them. The `loadViewComponentsAs` method accepts two arguments: the tag prefix for your view components and an array of your view component class names. For example, if your package's prefix is `courier` and you have `Alert` and `Button` view components, you would add the following to your service provider's `boot` method: -->
패키지에 [view components](/docs/8.x/blade#components)가 포함되어 있다면, `loadViewComponentsAs` 메서드를 통해 Laravel에 등록할 수 있습니다. `loadViewComponentsAs` 메서드는 컴포넌트 태그의 접두사, 그리고 컴포넌트 클래스명을 담은 배열을 받습니다. 예를 들어, 접두사가 `courier`이고 `Alert`, `Button` 컴포넌트가 있다면, 서비스 프로바이더의 `boot` 메서드에 아래처럼 추가합니다:

```
use Courier\Components\Alert;
use Courier\Components\Button;

/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewComponentsAs('courier', [
        Alert::class,
        Button::class,
    ]);
}
```

<!-- Once your view components are registered in a service provider, you may reference them in your view like so: -->
뷰 컴포넌트를 등록했다면, 뷰 파일에서 아래와 같이 사용할 수 있습니다:

```
<x-courier-alert />

<x-courier-button />
```

<a name="anonymous-components"></a>
<!-- #### Anonymous Components -->
#### Anonymous Components

<!-- If your package contains anonymous components, they must be placed within a `components` directory of your package's "views" directory (as specified by `loadViewsFrom`). Then, you may render them by prefixing the component name with the package's view namespace: -->
패키지에 익명 뷰 컴포넌트가 있다면, 반드시 패키지 "뷰" 디렉터리의 `components` 폴더 안에 위치해야 합니다 (`loadViewsFrom`에서 지정한 경로 내). 그런 다음, 컴포넌트 이름 앞에 패키지의 뷰 네임스페이스를 붙여서 아래와 같이 사용할 수 있습니다:

```
<x-courier::alert />
```

<a name="commands"></a>
<!-- ## Commands -->
## Commands

<!-- To register your package's Artisan commands with Laravel, you may use the `commands` method. This method expects an array of command class names. Once the commands have been registered, you may execute them using the [Artisan CLI](/docs/8.x/artisan): -->
패키지의 아티즌 명령어를 Laravel에 등록하려면, `commands` 메서드를 사용하세요. 이 메서드는 명령어 클래스명 배열을 인자로 받습니다. 등록이 완료된 후에는 [Artisan CLI](/docs/8.x/artisan)로 명령어를 실행할 수 있습니다:

```
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}
```

<a name="public-assets"></a>
<!-- ## Public Assets -->
## Public Assets

<!-- Your package may have assets such as JavaScript, CSS, and images. To publish these assets to the application's `public` directory, use the service provider's `publishes` method. In this example, we will also add a `public` asset group tag, which may be used to easily publish groups of related assets: -->
패키지에 JavaScript, CSS, 이미지 등 에셋 파일이 있다면, 서비스 프로바이더의 `publishes` 메서드를 사용해 애플리케이션의 `public` 디렉터리로 배포할 수 있습니다. 아래 예제에서는 `public` 에셋 그룹 태그도 함께 지정했는데, 이를 통해 관련 에셋들을 쉽게 함께 배포할 수 있습니다:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

<!-- Now, when your package's users execute the `vendor:publish` command, your assets will be copied to the specified publish location. Since users will typically need to overwrite the assets every time the package is updated, you may use the `--force` flag: -->
이제 패키지 사용자가 `vendor:publish` 명령어를 실행하면, 에셋이 지정한 위치로 복사됩니다. 패키지를 업데이트할 때마다 에셋을 덮어써야 할 경우가 많으므로, 아래처럼 `--force` 옵션을 사용할 수 있습니다:

```
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
<!-- ## Publishing File Groups -->
## Publishing File Groups

<!-- You may want to publish groups of package assets and resources separately. For instance, you might want to allow your users to publish your package's configuration files without being forced to publish your package's assets. You may do this by "tagging" them when calling the `publishes` method from a package's service provider. For example, let's use tags to define two publish groups for the `courier` package (`courier-config` and `courier-migrations`) in the `boot` method of the package's service provider: -->
패키지의 여러 에셋과 리소스를 원하는 그룹별로 따로 배포할 수 있습니다. 예를 들어, 사용자가 설정 파일만 배포하고 에셋은 따로 배포하지 않게 하고 싶을 수 있습니다. 이럴 때 패키지의 서비스 프로바이더에서 `publishes` 메서드를 호출할 때 "태그(tag)"를 지정해 여러 그룹을 정의할 수 있습니다. 아래는 `courier` 패키지에서 `courier-config`와 `courier-migrations`라는 두 배포 그룹을 `boot` 메서드에서 정의하는 예시입니다:

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishes([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

<!-- Now your users may publish these groups separately by referencing their tag when executing the `vendor:publish` command: -->
이제 사용자들은 `vendor:publish` 명령어를 실행할 때 원하는 태그를 지정해 그룹별로 선택적으로 배포할 수 있습니다:

```
php artisan vendor:publish --tag=courier-config
```
