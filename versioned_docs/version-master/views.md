# 뷰 (Views)

- [소개](#introduction)
    - [React / Svelte / Vue에서 뷰 작성하기](#writing-views-in-react-svelte-or-vue)
- [뷰 생성 및 렌더링](#creating-and-rendering-views)
    - [중첩된 뷰 디렉터리](#nested-view-directories)
    - [사용 가능한 첫 번째 뷰 생성](#creating-the-first-available-view)
    - [뷰 존재 여부 확인](#determining-if-a-view-exists)
- [뷰에 데이터 전달](#passing-data-to-views)
    - [모든 뷰에 데이터 공유](#sharing-data-with-all-views)
- [View Composer](#view-composers)
    - [View Creator](#view-creators)
- [뷰 최적화](#optimizing-views)

<a name="introduction"></a>
## 소개 (Introduction)

물론 라우트나 컨트롤러에서 전체 HTML 문서 문자열을 직접 반환하는 방식은 실용적이지 않습니다. 다행히도 **뷰(View)** 를 사용하면 모든 HTML을 별도의 파일로 분리하여 관리할 수 있습니다.

뷰는 컨트롤러 / 애플리케이션 로직과 화면 표시(presentation) 로직을 분리합니다. 뷰 파일은 `resources/views` 디렉터리에 저장됩니다. Laravel에서는 보통 [Blade 템플릿 언어](/docs/master/blade)를 사용하여 뷰 템플릿을 작성합니다. 간단한 뷰 예시는 다음과 같습니다.

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

이 뷰는 `resources/views/greeting.blade.php`에 저장되어 있으므로 다음과 같이 전역 `view` 헬퍼를 사용해 반환할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade 템플릿 작성 방법에 대해 더 알고 싶다면 전체 [Blade documentation](/docs/master/blade)을 참고하여 시작하십시오.

<a name="writing-views-in-react-svelte-or-vue"></a>
### React / Svelte / Vue에서 뷰 작성하기

많은 개발자들은 Blade를 사용해 PHP로 프런트엔드 템플릿을 작성하기보다는 React, Svelte, 또는 Vue를 사용해 템플릿을 작성하는 방식을 선호하기 시작했습니다. Laravel은 [Inertia](https://inertiajs.com/) 덕분에 이러한 방식을 매우 쉽게 구현할 수 있습니다. Inertia는 일반적인 SPA 구축 과정의 복잡함 없이 React / Svelte / Vue 프런트엔드를 Laravel 백엔드와 간단하게 연결할 수 있도록 해주는 라이브러리입니다.

Laravel의 [React, Svelte, Vue 애플리케이션 스타터 키트](/docs/master/starter-kits)는 Inertia 기반 Laravel 애플리케이션을 시작하기 위한 훌륭한 출발점을 제공합니다.

<a name="creating-and-rendering-views"></a>
## 뷰 생성 및 렌더링 (Creating and Rendering Views)

애플리케이션의 `resources/views` 디렉터리에 `.blade.php` 확장자를 가진 파일을 생성하거나 `make:view` Artisan 명령어를 사용하여 뷰를 생성할 수 있습니다.

```shell
php artisan make:view greeting
```

`.blade.php` 확장자는 해당 파일이 [Blade template](/docs/master/blade)를 포함하고 있음을 프레임워크에 알려줍니다. Blade 템플릿은 HTML과 함께 Blade 지시어(Directive)를 포함할 수 있으며, 이를 통해 값 출력, `if` 문 작성, 데이터 반복 처리 등을 쉽게 할 수 있습니다.

뷰를 생성한 후에는 전역 `view` 헬퍼를 사용하여 애플리케이션의 라우트나 컨트롤러에서 해당 뷰를 반환할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

또는 `View` 파사드(Facade)를 사용해 반환할 수도 있습니다.

```php
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

보시다시피 `view` 헬퍼의 첫 번째 인수는 `resources/views` 디렉터리에 있는 뷰 파일 이름에 해당합니다. 두 번째 인수는 뷰에서 사용할 데이터를 담은 배열입니다. 이 예제에서는 `name` 변수를 전달하고 있으며, 이는 뷰에서 [Blade 문법](/docs/master/blade)을 사용하여 출력됩니다.

<a name="nested-view-directories"></a>
### 중첩된 뷰 디렉터리

뷰는 `resources/views` 디렉터리 내부의 하위 디렉터리에 저장할 수도 있습니다. 중첩된 뷰를 참조할 때는 **점(dot) 표기법**을 사용할 수 있습니다.

예를 들어 뷰가 `resources/views/admin/profile.blade.php`에 있다면 다음과 같이 반환할 수 있습니다.

```php
return view('admin.profile', $data);
```

> [!WARNING]
> 뷰 디렉터리 이름에는 `.` 문자를 포함해서는 안 됩니다.

<a name="creating-the-first-available-view"></a>
### 사용 가능한 첫 번째 뷰 생성

`View` 파사드의 `first` 메서드를 사용하면 주어진 뷰 배열 중 **존재하는 첫 번째 뷰**를 생성할 수 있습니다. 이 기능은 애플리케이션이나 패키지에서 뷰를 사용자 정의하거나 덮어쓸 수 있도록 허용할 때 유용합니다.

```php
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
### 뷰 존재 여부 확인

뷰가 존재하는지 확인해야 할 경우 `View` 파사드를 사용할 수 있습니다. `exists` 메서드는 뷰가 존재하면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
## 뷰에 데이터 전달 (Passing Data to Views)

앞의 예제에서 보았듯이, 배열 형태의 데이터를 전달하여 뷰에서 사용할 수 있게 만들 수 있습니다.

```php
return view('greetings', ['name' => 'Victoria']);
```

이 방식으로 데이터를 전달할 때는 **키 / 값 쌍(key / value pairs)** 을 가진 배열이어야 합니다. 뷰에 데이터를 전달하면 뷰 내부에서 해당 키를 사용하여 값에 접근할 수 있습니다. 예를 들어 `<?php echo $name; ?>`과 같이 사용할 수 있습니다.

또 다른 방법으로, `view` 헬퍼에 전체 배열을 전달하는 대신 `with` 메서드를 사용해 개별 데이터를 추가할 수도 있습니다. `with` 메서드는 뷰 객체 인스턴스를 반환하므로 메서드 체이닝을 계속 사용할 수 있습니다.

```php
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
### 모든 뷰에 데이터 공유

경우에 따라 애플리케이션에서 렌더링되는 **모든 뷰에 동일한 데이터를 공유**해야 할 때가 있습니다. 이 경우 `View` 파사드의 `share` 메서드를 사용할 수 있습니다.

일반적으로 `share` 메서드는 서비스 프로바이더의 `boot` 메서드 내부에 작성합니다. `App\Providers\AppServiceProvider` 클래스에 추가하거나 별도의 서비스 프로바이더를 생성하여 관리할 수 있습니다.

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
## View Composer

View Composer는 뷰가 렌더링될 때 호출되는 콜백 또는 클래스 메서드입니다. 특정 뷰가 렌더링될 때마다 데이터를 바인딩해야 한다면 View Composer를 사용해 해당 로직을 하나의 위치에 정리할 수 있습니다. 특히 하나의 뷰가 여러 라우트나 컨트롤러에서 반환되며 항상 동일한 데이터가 필요할 때 유용합니다.

일반적으로 View Composer는 애플리케이션의 [service providers](/docs/master/providers) 중 하나에 등록합니다. 이 예제에서는 `App\Providers\AppServiceProvider`에 등록한다고 가정합니다.

`View` 파사드의 `composer` 메서드를 사용해 View Composer를 등록할 수 있습니다. Laravel에는 클래스 기반 View Composer를 위한 기본 디렉터리가 제공되지 않으므로 원하는 구조로 자유롭게 정리할 수 있습니다. 예를 들어 `app/View/Composers` 디렉터리를 만들어 모든 View Composer를 저장할 수 있습니다.

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

Composer를 등록하면 `profile` 뷰가 렌더링될 때마다 `App\View\Composers\ProfileComposer` 클래스의 `compose` 메서드가 실행됩니다. Composer 클래스 예시는 다음과 같습니다.

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

모든 View Composer는 [service container](/docs/master/container)를 통해 해결(resolve)되므로 Composer 생성자에서 필요한 의존성을 타입 힌트로 선언할 수 있습니다.

<a name="attaching-a-composer-to-multiple-views"></a>
#### 여러 뷰에 Composer 연결

`composer` 메서드의 첫 번째 인수로 **뷰 배열**을 전달하면 하나의 View Composer를 여러 뷰에 동시에 연결할 수 있습니다.

```php
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

또한 `composer` 메서드는 와일드카드 `*`를 지원하므로 모든 뷰에 Composer를 연결할 수도 있습니다.

```php
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
### View Creator

View "Creator"는 View Composer와 매우 유사하지만, **뷰가 렌더링되기 직전이 아니라 뷰 인스턴스가 생성되는 즉시 실행**된다는 차이가 있습니다.

View Creator를 등록하려면 `creator` 메서드를 사용합니다.

```php
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
## 뷰 최적화 (Optimizing Views)

기본적으로 Blade 템플릿 뷰는 **요청 시(on demand)** 컴파일됩니다. 뷰를 렌더링하는 요청이 실행되면 Laravel은 먼저 컴파일된 뷰가 존재하는지 확인합니다. 파일이 존재하면 **컴파일되지 않은 원본 뷰가 컴파일된 뷰보다 더 최근에 수정되었는지** 확인합니다. 만약 컴파일된 뷰가 없거나 원본 뷰가 더 최근에 수정되었다면 Laravel은 뷰를 다시 컴파일합니다.

요청 중에 뷰를 컴파일하면 성능에 약간의 영향을 줄 수 있습니다. 따라서 Laravel은 애플리케이션에서 사용하는 모든 뷰를 **미리 컴파일(precompile)** 할 수 있도록 `view:cache` Artisan 명령어를 제공합니다. 성능 향상을 위해 배포 과정(deployment process)의 일부로 이 명령어를 실행하는 것이 좋습니다.

```shell
php artisan view:cache
```

뷰 캐시를 삭제하려면 `view:clear` 명령어를 사용하면 됩니다.

```shell
php artisan view:clear
```