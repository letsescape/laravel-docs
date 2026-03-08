# 뷰 (Views)

- [소개](#introduction)
    - [React / Svelte / Vue로 뷰 작성하기](#writing-views-in-react-svelte-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩 뷰 디렉토리](#nested-view-directories)
    - [가장 먼저 존재하는 뷰 생성하기](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달](#passing-data-to-views)
    - [모든 뷰에 데이터 공유하기](#sharing-data-with-all-views)
- [뷰 컴포저](#view-composers)
    - [뷰 크리에이터](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

라우트(route)나 컨트롤러(controller)에서 HTML 문서 전체를 문자열로 직접 반환하는 것은 비효율적입니다. 다행히도, 뷰(View)를 사용하면 모든 HTML을 별도의 파일에 편리하게 분리할 수 있습니다.

뷰는 컨트롤러/애플리케이션 로직과 프레젠테이션(출력) 로직을 분리해 주며, `resources/views` 디렉토리에 저장됩니다. Laravel을 사용할 때 뷰 템플릿은 주로 [Blade 템플릿 언어](/docs/12.x/blade)를 이용해 작성합니다. 간단한 뷰 예시는 다음과 같습니다:

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰가 `resources/views/greeting.blade.php`에 저장되어 있으므로, 아래와 같이 전역 `view` 헬퍼로 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성법에 대해 더 알고 싶으시다면, [Blade 공식 문서](/docs/12.x/blade)를 참고해 시작해 보시기 바랍니다.

<a name="writing-views-in-react-svelte-or-vue"></a>
### React / Svelte / Vue로 뷰 작성하기

많은 개발자들이 Blade를 이용한 PHP 기반의 프론트엔드 템플릿 대신, React, Svelte, 또는 Vue를 사용해 뷰(템플릿)를 작성하는 방식을 선호하고 있습니다. Laravel은 [Inertia](https://inertiajs.com/)라는 라이브러리를 통해 이 작업을 매우 간편하게 만들었습니다. Inertia를 사용하면 React / Svelte / Vue 프런트엔드를 Laravel 백엔드와 쉽게 연결할 수 있으며, SPA(싱글 페이지 애플리케이션)를 구축할 때의 복잡함을 크게 줄여줍니다.

Laravel의 [React, Svelte, Vue 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 활용하면, Inertia로 구동되는 새로운 Laravel 애플리케이션의 시작점을 빠르게 만들 수 있습니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

뷰 파일은 애플리케이션의 `resources/views` 디렉토리에 `.blade.php` 확장자로 직접 생성하거나, `make:view` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade 템플릿](/docs/12.x/blade)임을 프레임워크에 알려줍니다. Blade 템플릿에는 HTML과 Blade 지시문(디렉티브)이 함께 포함될 수 있어, 값을 출력하거나, if문 작성, 데이터 반복 등 다양한 로직을 쉽게 구현할 수 있습니다.

뷰를 생성했다면, 해당 뷰는 애플리케이션의 라우트나 컨트롤러에서 전역 `view` 헬퍼로 반환할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또는 `View` 파사드(Facade)를 이용해 반환할 수도 있습니다:

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

여기서 `view` 헬퍼의 첫 번째 인수는 `resources/views` 디렉토리 내 뷰 파일의 이름을 의미합니다. 두 번째 인수는 뷰에서 사용할 데이터를 배열로 전달하는 부분입니다. 이번 예시에서는 `name` 변수를 전달하고 있으며, 뷰에서는 [Blade 문법](/docs/12.x/blade)을 통해 출력합니다.

<a name="nested-view-directories"></a>
### 중첩 뷰 디렉토리

뷰 파일은 `resources/views` 디렉토리의 하위 폴더(서브디렉토리)에도 저장할 수 있습니다. 중첩 뷰를 참조할 때는 "점(.) 표기법"을 사용합니다. 예를 들어, `resources/views/admin/profile.blade.php`에 뷰가 있다면 다음과 같이 반환할 수 있습니다:

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉토리 이름에는 `.` 문자를 포함해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 가장 먼저 존재하는 뷰 생성하기

`View` 파사드의 `first` 메서드를 사용하면, 주어진 뷰 목록 중에서 실제로 존재하는 가장 첫 번째 뷰를 반환할 수 있습니다. 이는 애플리케이션이나 패키지에서 뷰를 커스터마이즈(재정의)할 때 유용하게 활용됩니다:

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

특정 뷰 파일이 실제로 존재하는지 확인하려면 `View` 파사드를 사용할 수 있습니다. `exists` 메서드는 뷰가 있으면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달 (Passing Data to Views)

앞선 예시들처럼, 뷰로 전달하고 싶은 데이터는 배열 형태로 넘길 수 있습니다. 그러면 그 데이터들을 뷰에서 사용할 수 있습니다:

```php
return view('greetings', ['name' => 'Victoria']);
```

이 방식에서 전달하는 데이터는 key/value(키/값) 형태의 배열이어야 합니다. 데이터를 뷰로 전달하면, 각 키를 통해 뷰 내에서 해당 데이터를 참조할 수 있습니다. 예를 들어 `<?php echo $name; ?>` 처럼 사용할 수 있습니다.

또는, `view` 헬퍼 함수 대신 체이닝 가능한 `with` 메서드로 각각의 데이터를 추가하는 방법도 있습니다. `with` 메서드는 뷰 객체의 인스턴스를 반환하므로, 반환 전에 추가 메서드 체이닝이 가능합니다:

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유하기

때때로, 애플리케이션에서 렌더링되는 모든 뷰에 데이터를 공유해야 할 때가 있습니다. 이럴 때는 `View` 파사드의 `share` 메서드를 사용하면 됩니다. 보통은 서비스 프로바이더의 `boot` 메서드에서 이 메서드를 호출하는 것이 좋습니다. `App\Providers\AppServiceProvider` 클래스에 추가할 수 있고, 별도의 서비스 프로바이더를 만들어서 관리해도 됩니다:

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
## 뷰 컴포저 (View Composers)

뷰 컴포저는 뷰가 렌더링될 때마다 호출되는 콜백(함수) 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 항상 데이터를 묶어서 전달하고 싶다면, 뷰 컴포저를 사용해서 해당 로직을 한 곳에 모아놓을 수 있습니다. 같은 뷰가 여러 라우트나 컨트롤러에서 반복적으로 사용되고, 일정한 데이터가 항상 필요할 때 특히 유용합니다.

일반적으로 뷰 컴포저는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers)에서 등록합니다. 아래 예시에서는 `App\Providers\AppServiceProvider`에서 관련 로직을 관리한다고 가정합니다.

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
        // 클래스 기반 컴포저 사용
        Facades\View::composer('profile', ProfileComposer::class);

        // 클로저(익명 함수) 기반 컴포저 사용
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

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

보시는 것처럼, 모든 뷰 컴포저는 [서비스 컨테이너](/docs/12.x/container)를 통해 의존성 주입을 지원하므로, 생성자에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 하나의 컴포저를 여러 뷰에 연결하기

하나의 뷰 컴포저를 여러 뷰에 동시에 연결하려면, `composer` 메서드의 첫 번째 인수로 뷰들의 배열을 전달하면 됩니다:

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한, `composer` 메서드는 와일드카드로 `*` 문자를 지원하여, 모든 뷰에 컴포저를 연결할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### 뷰 크리에이터 (View Creators)

뷰 "크리에이터(creator)"는 뷰 컴포저와 매우 유사하지만, 뷰가 렌더링되기 직전이 아니라 뷰 인스턴스가 생성되자마자 즉시 실행된다는 점이 다릅니다. 뷰 크리에이터를 등록하려면 `creator` 메서드를 사용합니다:

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화 (Optimizing Views)

기본적으로 Blade 템플릿 뷰는 요청이 들어올 때마다 필요할 때마다 컴파일됩니다. 요청 과정에서 뷰를 렌더링하게 되면, Laravel은 컴파일된 뷰 파일이 존재하는지 확인합니다. 파일이 존재하면, 원본(View) 파일이 더 최근에 수정됐는지 확인해, 필요하면 다시 컴파일합니다. 만약 컴파일된 파일이 없거나, 원본이 수정됐다면, Laravel은 뷰를 다시 컴파일합니다.

이러한 컴파일 과정이 요청 처리 중에 수행되면, 성능에 미세한 영향을 미칠 수 있습니다. 이를 최적화하려면, `view:cache` Artisan 명령어로 애플리케이션에서 사용하는 모든 뷰를 미리 한 번에 컴파일할 수 있습니다. 성능 향상을 위해 배포 프로세스(deployment 과정)의 일부로 이 명령어를 실행하는 것이 좋습니다:

```shell
php artisan view:cache
```

뷰 캐시를 지우려면 `view:clear` 명령어를 사용할 수 있습니다:

```shell
php artisan view:clear
```