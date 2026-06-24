<!-- # Views -->
# Views

- [Introduction](#introduction)
    - [Writing Views in React / Svelte / Vue](#writing-views-in-react-svelte-or-vue)
- [Creating and Rendering Views](#creating-and-rendering-views)
    - [Nested View Directories](#nested-view-directories)
    - [Creating the First Available View](#creating-the-first-available-view)
    - [Determining if a View Exists](#determining-if-a-view-exists)
- [Passing Data to Views](#passing-data-to-views)
    - [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
    - [View Creators](#view-creators)
- [Optimizing Views](#optimizing-views)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Of course, it's not practical to return entire HTML documents strings directly from your routes and controllers. Thankfully, views provide a convenient way to place all of our HTML in separate files. -->
라우트(route)나 컨트롤러(controller)에서 HTML 문서 전체를 문자열로 직접 반환하는 것은 비효율적입니다. 다행히도, 뷰(View)를 사용하면 모든 HTML을 별도의 파일에 편리하게 분리할 수 있습니다.

<!-- Views separate your controller / application logic from your presentation logic and are stored in the `resources/views` directory. When using Laravel, view templates are usually written using the [Blade templating language](/docs/12.x/blade). A simple view might look something like this: -->
뷰는 컨트롤러/애플리케이션 로직과 프레젠테이션(출력) 로직을 분리해 주며, `resources/views` 디렉토리에 저장됩니다. Laravel을 사용할 때 뷰 템플릿은 주로 [Blade templating language](/docs/12.x/blade)를 이용해 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

<!-- Since this view is stored at `resources/views/greeting.blade.php`, we may return it using the global `view` helper like so: -->
이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 아래와 같이 전역 `view` 헬퍼로 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성법에 대해 더 알고 싶으시다면, [Blade documentation](/docs/12.x/blade)를 참고해 시작해 보시기 바랍니다.

<a name="writing-views-in-react-svelte-or-vue"></a>
<!-- ### Writing Views in React / Svelte / Vue -->
### Writing Views in React / Svelte / Vue

<!-- Instead of writing their frontend templates in PHP via Blade, many developers have begun to prefer to write their templates using React, Svelte, or Vue. Laravel makes this painless thanks to [Inertia](https://inertiajs.com/), a library that makes it a cinch to tie your React / Svelte / Vue frontend to your Laravel backend without the typical complexities of building an SPA. -->
많은 개발자들이 Blade를 이용한 PHP 기반의 프론트엔드 템플릿 대신, React, Svelte, 또는 Vue를 사용해 뷰(템플릿)를 작성하는 방식을 선호하고 있습니다. Laravel은 [Inertia](https://inertiajs.com/)라는 라이브러리를 통해 이 작업을 매우 간편하게 만들었습니다. Inertia를 사용하면 React / Svelte / Vue 프런트엔드를 Laravel 백엔드와 쉽게 연결할 수 있으며, SPA(싱글 페이지 애플리케이션)를 구축할 때의 복잡함을 크게 줄여줍니다.

<!-- Our [React, Svelte, and Vue application starter kits](/docs/12.x/starter-kits) give you a great starting point for your next Laravel application powered by Inertia. -->
Laravel의 [React, Svelte, and Vue application starter kits](/docs/12.x/starter-kits)를 활용하면, Inertia로 구동되는 새로운 Laravel 애플리케이션의 시작점을 빠르게 만들 수 있습니다.

<a name="creating-and-rendering-views"></a>
<!-- ## Creating and Rendering Views -->
## Creating and Rendering Views

<!-- You may create a view by placing a file with the `.blade.php` extension in your application's `resources/views` directory or by using the `make:view` Artisan command: -->
뷰 파일은 애플리케이션의 `resources/views` 디렉토리에 `.blade.php` 확장자로 직접 생성하거나, `make:view` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

<!-- The `.blade.php` extension informs the framework that the file contains a [Blade template](/docs/12.x/blade). Blade templates contain HTML as well as Blade directives that allow you to easily echo values, create "if" statements, iterate over data, and more. -->
`.blade.php` 확장자는 해당 파일이 [Blade template](/docs/12.x/blade)임을 프레임워크에 알려줍니다. Blade 템플릿에는 HTML과 Blade 지시문(디렉티브)이 함께 포함될 수 있어, 값을 출력하거나, if문 작성, 데이터 반복 등 다양한 로직을 쉽게 구현할 수 있습니다.

<!-- Once you have created a view, you may return it from one of your application's routes or controllers using the global `view` helper: -->
뷰를 생성했다면, 해당 뷰는 애플리케이션의 라우트나 컨트롤러에서 전역 `view` 헬퍼로 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

<!-- Views may also be returned using the `View` facade: -->
또는 `View` 파사드(Facade)를 이용해 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

<!-- As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument is an array of data that should be made available to the view. In this case, we are passing the `name` variable, which is displayed in the view using [Blade syntax](/docs/12.x/blade). -->
여기서 `view` 헬퍼의 첫 번째 인수는 `resources/views` 디렉토리 내 뷰 파일의 이름을 의미합니다. 두 번째 인수는 뷰에서 사용할 데이터를 배열로 전달하는 부분입니다. 이번 예시에서는 `name` 변수를 전달하고 있으며, 뷰에서는 [Blade syntax](/docs/12.x/blade)을 통해 출력합니다.

<a name="nested-view-directories"></a>
<!-- ### Nested View Directories -->
### Nested View Directories

<!-- Views may also be nested within subdirectories of the `resources/views` directory. "Dot" notation may be used to reference nested views. For example, if your view is stored at `resources/views/admin/profile.blade.php`, you may return it from one of your application's routes / controllers like so: -->
뷰 파일은 `resources/views` 디렉토리의 하위 폴더(서브디렉토리)에도 저장할 수 있습니다. 중첩 뷰를 참조할 때는 "점(.) 표기법"을 사용합니다. 예를 들어, `resources/views/admin/profile.blade.php`에 뷰가 있다면 다음과 같이 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉토리 이름에는 `.` 문자를 포함해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
<!-- ### Creating the First Available View -->
### Creating the First Available View

<!-- Using the `View` facade's `first` method, you may create the first view that exists in a given array of views. This may be useful if your application or package allows views to be customized or overwritten: -->
`View` 파사드의 `first` 메서드를 사용하면, 주어진 뷰 목록 중에서 실제로 존재하는 가장 첫 번째 뷰를 반환할 수 있습니다. 이는 애플리케이션이나 패키지에서 뷰를 사용자 지정(재정의)할 때 유용하게 활용됩니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
<!-- ### Determining if a View Exists -->
### Determining if a View Exists

<!-- If you need to determine if a view exists, you may use the `View` facade. The `exists` method will return `true` if the view exists: -->
특정 뷰 파일이 실제로 존재하는지 확인하려면 `View` 파사드를 사용할 수 있습니다. `exists` 메서드는 뷰가 있으면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
<!-- ## Passing Data to Views -->
## Passing Data to Views

<!-- As you saw in the previous examples, you may pass an array of data to views to make that data available to the view: -->
앞선 예시들처럼, 뷰로 전달하고 싶은 데이터는 배열 형태로 넘길 수 있습니다. 그러면 그 데이터들을 뷰에서 사용할 수 있습니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

<!-- When passing information in this manner, the data should be an array with key / value pairs. After providing data to a view, you can then access each value within your view using the data's keys, such as `<?php echo $name; ?>`. -->
이 방식에서 전달하는 데이터는 key/value(키/값) 형태의 배열이어야 합니다. 데이터를 뷰로 전달하면, 각 키를 통해 뷰 내에서 해당 데이터를 참조할 수 있습니다. 예를 들어 `<?php echo $name; ?>` 처럼 사용할 수 있습니다.

<!-- As an alternative to passing a complete array of data to the `view` helper function, you may use the `with` method to add individual pieces of data to the view. The `with` method returns an instance of the view object so that you can continue chaining methods before returning the view: -->
또는, `view` 헬퍼 함수 대신 체이닝 가능한 `with` 메서드로 각각의 데이터를 추가하는 방법도 있습니다. `with` 메서드는 뷰 객체의 인스턴스를 반환하므로, 반환 전에 추가 메서드 체이닝이 가능합니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
<!-- ### Sharing Data With All Views -->
### Sharing Data With All Views

<!-- Occasionally, you may need to share data with all views that are rendered by your application. You may do so using the `View` facade's `share` method. Typically, you should place calls to the `share` method within a service provider's `boot` method. You are free to add them to the `App\Providers\AppServiceProvider` class or generate a separate service provider to house them: -->
때때로, 애플리케이션에서 렌더링되는 모든 뷰에 데이터를 공유해야 할 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용하면 됩니다. 보통은 서비스 프로바이더의 `boot` 메서드에서 `share` 메서드를 호출하는 것이 좋습니다. `App\Providers\AppServiceProvider` 클래스에 추가할 수 있고, 별도의 서비스 프로바이더를 만들어서 관리해도 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
<!-- ## View Composers -->
## View Composers

<!-- View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want to be bound to a view each time that view is rendered, a view composer can help you organize that logic into a single location. View composers may prove particularly useful if the same view is returned by multiple routes or controllers within your application and always needs a particular piece of data. -->
뷰 컴포저는 뷰가 렌더링될 때마다 호출되는 콜백(함수) 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 항상 데이터를 묶어서 전달하고 싶다면, 뷰 컴포저를 사용해서 해당 로직을 한 곳에 모아놓을 수 있습니다. 같은 뷰가 여러 라우트나 컨트롤러에서 반복적으로 사용되고, 일정한 데이터가 항상 필요할 때 특히 유용합니다.

<!-- Typically, view composers will be registered within one of your application's [service providers](/docs/12.x/providers). In this example, we'll assume that the `App\Providers\AppServiceProvider` will house this logic. -->
일반적으로 뷰 컴포저는 애플리케이션의 [service providers](/docs/12.x/providers)에서 등록합니다. 아래 예시에서는 `App\Providers\AppServiceProvider`에서 관련 로직을 관리한다고 가정합니다.

<!-- We'll use the `View` facade's `composer` method to register the view composer. Laravel does not include a default directory for class-based view composers, so you are free to organize them however you wish. For example, you could create an `app/View/Composers` directory to house all of your application's view composers: -->
`View` 파사드의 `composer` 메서드를 이용해 뷰 컴포저를 등록할 수 있습니다. Laravel은 클래스 기반 뷰 컴포저의 기본 디렉토리를 제공하지 않으므로, 여러분이 원하는 구조로 코드를 관리하시면 됩니다. 예를 들어, 모든 컴포저 클래스를 `app/View/Composers` 디렉토리에 둘 수 있습니다:

```php
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // Using class-based composers...
        Facades\View::composer('profile', ProfileComposer::class);

        // Using closure-based composers...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

<!-- Now that we have registered the composer, the `compose` method of the `App\View\Composers\ProfileComposer` class will be executed each time the `profile` view is being rendered. Let's take a look at an example of the composer class: -->
컴포저를 등록한 후에는, `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 `profile` 뷰가 렌더링될 때마다 실행됩니다. 컴포저 클래스의 예시는 아래와 같습니다:

```php
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * Create a new profile composer.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * Bind data to the view.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

<!-- As you can see, all view composers are resolved via the [service container](/docs/12.x/container), so you may type-hint any dependencies you need within a composer's constructor. -->
보시는 것처럼, 모든 뷰 컴포저는 [service container](/docs/12.x/container)를 통해 의존성 주입을 지원하므로, 생성자에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
<!-- #### Attaching a Composer to Multiple Views -->
#### Attaching a Composer to Multiple Views

<!-- You may attach a view composer to multiple views at once by passing an array of views as the first argument to the `composer` method: -->
하나의 뷰 컴포저를 여러 뷰에 동시에 연결하려면, `composer` 메서드의 첫 번째 인수로 뷰들의 배열을 전달하면 됩니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

<!-- The `composer` method also accepts the `*` character as a wildcard, allowing you to attach a composer to all views: -->
또한, `composer` 메서드는 와일드카드로 `*` 문자를 지원하여, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
<!-- ### View Creators -->
### View Creators

<!-- View "creators" are very similar to view composers; however, they are executed immediately after the view is instantiated instead of waiting until the view is about to render. To register a view creator, use the `creator` method: -->
뷰 "크리에이터(creator)"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아니라 뷰 인스턴스가 생성되자마자 즉시 실행된다는 점이 다릅니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
<!-- ## Optimizing Views -->
## Optimizing Views

<!-- By default, Blade template views are compiled on demand. When a request is executed that renders a view, Laravel will determine if a compiled version of the view exists. If the file exists, Laravel will then determine if the uncompiled view has been modified more recently than the compiled view. If the compiled view either does not exist, or the uncompiled view has been modified, Laravel will recompile the view. -->
기본적으로 Blade 템플릿 뷰는 요청이 들어올 때마다 필요할 때마다 컴파일됩니다. 요청 과정에서 뷰를 렌더링하게 되면, Laravel은 컴파일된 뷰 파일이 존재하는지 확인합니다. 파일이 존재하면, 원본(View) 파일이 더 최근에 수정됐는지 확인해, 필요하면 다시 컴파일합니다. 만약 컴파일된 파일이 없거나, 원본이 수정됐다면, Laravel은 뷰를 다시 컴파일합니다.

<!-- Compiling views during the request may have a small negative impact on performance, so Laravel provides the `view:cache` Artisan command to precompile all of the views utilized by your application. For increased performance, you may wish to run this command as part of your deployment process: -->
이러한 컴파일 과정이 요청 처리 중에 수행되면, 성능에 미세한 영향을 미칠 수 있습니다. 이를 최적화하려면, `view:cache` Artisan 명령어로 애플리케이션에서 사용하는 모든 뷰를 미리 한 번에 컴파일할 수 있습니다. 성능 향상을 위해 배포 프로세스(deployment 과정)의 일부로 이 명령어를 실행하는 것이 좋습니다:

```shell
php artisan view:cache
```

<!-- You may use the `view:clear` command to clear the view cache: -->
뷰 캐시를 지우려면 `view:clear` 명령어를 사용할 수 있습니다:

```shell
php artisan view:clear
```
