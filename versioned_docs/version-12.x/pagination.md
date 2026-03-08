# 데이터베이스: 페이징 처리 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이징 처리](#paginating-query-builder-results)
    - [Eloquent 결과 페이징 처리](#paginating-eloquent-results)
    - [커서 기반 페이징 처리](#cursor-pagination)
    - [페이징 처리 객체 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스터마이즈](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 범위 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스터마이즈](#customizing-the-pagination-view)
    - [Bootstrap 사용](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크에서는 페이징 처리(pagination)가 매우 번거로울 수 있습니다. Laravel의 페이징 처리 방식이 새로운 시도가 되기를 바랍니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/12.x/queries) 및 [Eloquent ORM](/docs/12.x/eloquent)과 통합되어 있으며, 설정 없이 데이터베이스 레코드를 쉽게 페이징 처리할 수 있습니다.

기본적으로 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환됩니다. 또한 Bootstrap 기반의 페이징 처리 뷰도 지원합니다.

<a name="tailwind"></a>
#### Tailwind

Laravel의 기본 Tailwind 페이지네이션 뷰를 Tailwind 4.x와 함께 사용한다면, 애플리케이션의 `resources/css/app.css` 파일이 이미 적절하게 설정되어 Laravel의 페이지네이션 뷰를 `@source`로 포함하고 있습니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이징 처리

항목을 페이징 처리하는 방법에는 여러 가지가 있지만, 가장 간단한 방법은 [쿼리 빌더](/docs/12.x/queries)나 [Eloquent 쿼리](/docs/12.x/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 현재 보고 있는 페이지에 따라 쿼리의 "limit"과 "offset"을 자동으로 설정합니다. 기본적으로 현재 페이지는 HTTP 요청의 쿼리 문자열 인수인 `page` 값으로 감지됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

아래 예시에서는 `paginate` 메서드에 "페이지당 표시할 항목 개수"만 인수로 전달합니다. 여기서는 페이지당 `15`개 항목을 표시하도록 지정하겠습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자 조회.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a name="simple-pagination"></a>
#### 단순 페이징 처리

`paginate` 메서드는 쿼리에 일치하는 전체 레코드 수를 먼저 카운트한 뒤, 레코드를 데이터베이스에서 조회합니다. 페이지네이터가 전체 페이지 수를 알기 위해서입니다. 하지만 애플리케이션 UI에 전체 페이지 개수를 표시할 계획이 없다면, 이 레코드 카운트 쿼리는 불필요합니다.

따라서, 애플리케이션의 UI에서 단순히 "다음" 및 "이전" 링크만 보여주고 싶다면, 효율적인 단일 쿼리를 수행하는 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이징 처리

[Eloquent](/docs/12.x/eloquent) 쿼리도 페이징 처리가 가능합니다. 다음 예시에서 `App\Models\User` 모델을 페이징 처리하고, 페이지당 15개 레코드를 표시하도록 지정합니다. 쿼리 빌더로 페이징 처리하는 것과 거의 동일한 문법을 사용합니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, 쿼리에 `where` 절 등 다른 조건을 추가한 뒤 `paginate` 메서드를 호출할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이징 처리할 때도 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

또한 Eloquent 모델을 커서 기반으로 페이징 처리할 때 `cursorPaginate` 메서드도 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에 여러 페이지네이터 인스턴스 사용

하나의 화면에서 두 개 이상의 서로 다른 페이지네이터를 렌더링해야 할 때도 있습니다. 하지만 두 페이지네이터가 모두 `page` 쿼리 문자열 파라미터를 사용해 현재 페이지를 저장하면 서로 충돌이 발생합니다. 이 경우, `paginate`, `simplePaginate`, `cursorPaginate` 메서드의 세 번째 인수에 원하는 쿼리 문자열 파라미터 이름을 전달하면 각 페이지네이터의 현재 페이지를 별도로 관리할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 기반 페이징 처리

`paginate`와 `simplePaginate`는 SQL의 "offset" 절을 사용하여 쿼리를 만듭니다. 이에 비해 커서 기반 페이징 처리는 정렬된 컬럼 값의 조건을 비교하는 "where" 절을 통해 쿼리를 만들기 때문에 Laravel의 모든 페이징 처리 방식 중에서 성능이 가장 뛰어납니다. 커서 기반 방식은 대용량 데이터셋과 "무한 스크롤" UI에 특히 적합합니다.

offset 기반 페이징 처리와 달리, 페이지네이터에서 생성되는 URL의 쿼리 문자열에 페이지 번호 대신 "커서(cursor)" 문자열이 포함됩니다. 커서는 인코딩된 문자열이며, 다음 페이징 쿼리가 어디에서부터 시작해야 할지와 어떤 방향으로 페이징할지에 대한 정보를 담고 있습니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 사용해 커서 기반 페이지네이터 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 가져온 후에는, `paginate` 및 `simplePaginate` 메서드를 사용할 때와 동일하게 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터에서 제공하는 인스턴스 메서드에 대한 더 자세한 정보는 [커서 페이지네이터 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하시기 바랍니다.

> [!WARNING]
> 커서 기반 페이징을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어야 합니다. 또한 쿼리에서 정렬되는 컬럼은 페이징 처리하려는 테이블에 반드시 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이징과 오프셋 페이징 비교

offset 페이징과 커서 페이징의 차이를 설명하기 위해, 아래와 같이 예시 SQL 쿼리를 살펴보겠습니다. 두 쿼리는 모두 `users` 테이블에서 `id` 기준으로 정렬된 "두 번째 페이지" 결과를 조회합니다:

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이징 쿼리는 offset 페이징 대비 다음과 같은 장점이 있습니다:

- 대용량 데이터셋의 경우, "order by" 컬럼이 인덱싱되어 있다면 커서 페이징이 더 좋은 성능을 제공합니다. 이는 "offset" 절이 이전에 일치하는 모든 데이터를 탐색하기 때문입니다.
- 데이터가 자주 변경(추가/삭제)되는 상황에서, offset 페이징은 사용자가 보고 있는 페이지에 최근에 레코드가 추가되거나 삭제되면 레코드 누락 또는 중복 표시 문제가 생길 수 있습니다.

하지만 커서 페이징에는 다음과 같은 제한 사항도 있습니다:

- `simplePaginate`와 마찬가지로 커서 페이징은 "다음", "이전" 링크 표시만 가능하며, 페이지 번호 링크 생성은 지원하지 않습니다.
- 적어도 하나 이상의 유니크한 컬럼을 기준으로 정렬해야 하며, 정렬 컬럼에 `null` 값이 있으면 사용할 수 없습니다.
- "order by" 절에 사용된 쿼리 표현식은 별칭(alias)으로 지정해서 "select" 절에도 반드시 포함시켜야 합니다.
- 파라미터가 포함된 쿼리 표현식은 지원되지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이징 처리 객체 수동 생성

간혹 이미 메모리에 있는 항목 배열로 페이징 객체를 수동으로 생성해야 할 때도 있습니다. 이때는 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스 중 하나를 직접 생성할 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 집합의 전체 항목 수를 몰라도 되지만, 이 때문에 마지막 페이지 인덱스를 가져오는 메서드는 제공하지 않습니다. `LengthAwarePaginator`는 `Paginator`와 거의 동일한 인수를 받지만, 전체 결과 수(total)가 필요합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate` 메서드, `CursorPaginator`는 `cursorPaginate` 메서드, 그리고 `LengthAwarePaginator`는 `paginate` 메서드에 각각 대응합니다.

> [!WARNING]
> 페이징 객체를 직접 생성할 때는 전달할 결과 배열을 직접 "슬라이스(slice)"해야 합니다. 방법을 잘 모르겠다면 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스터마이즈

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI와 동일하게 설정됩니다. 하지만 페이지네이터의 `withPath` 메서드를 사용하면, 페이지네이터가 링크를 생성할 때 사용할 URI를 커스터마이즈할 수 있습니다. 예를 들어, 페이지네이션 링크가 `http://example.com/admin/users?page=N`과 같이 생성되길 원한다면 `withPath` 메서드에 `/admin/users`를 전달하면 됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가

`appends` 메서드를 사용해 페이지네이션 링크의 쿼리 문자열에 값을 추가할 수 있습니다. 예를 들어, 각 페이지네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 `appends`를 호출합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청의 쿼리 문자열 값 전체를 페이지네이션 링크에 모두 추가하고 싶다면, `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가

페이지네이터가 생성하는 URL 끝에 "해시 프래그먼트"를 추가하려면, `fragment` 메서드를 사용할 수 있습니다. 예를 들어 각 페이지네이션 링크 끝에 `#users`를 추가하려면 아래와 같이 `fragment` 메서드를 사용합니다:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시 (Displaying Pagination Results)

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를 반환합니다. 그리고 마지막으로, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합을 설명하는 여러 메서드를 제공합니다. 또한, 페이지네이터 인스턴스는 반복(iterable) 객체이므로 배열처럼 순회할 수 있습니다. 즉, 결과를 가져온 뒤 [Blade](/docs/12.x/blade)를 사용해 결과 표시와 페이지 링크 렌더링이 가능합니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지로 이동할 수 있는 링크들을 렌더링합니다. 각 링크는 적절한 `page` 쿼리 문자열 변수를 이미 포함합니다. 참고로, `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환됩니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 범위 조정

페이지네이터가 페이지네이션 링크를 표시할 때, 현재 페이지 번호와 더불어 현재 페이지 기준 앞뒤로 최대 3개의 페이지 링크가 표시됩니다. `onEachSide` 메서드를 사용하면, 중앙 슬라이딩 윈도우 영역에 현재 페이지 기준으로 양쪽에 몇 개의 추가 링크를 표시할지 제어할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환

Laravel의 페이지네이터 클래스들은 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하고 있으며, `toJson` 메서드를 통해 쉽게 결과를 JSON으로 변환할 수 있습니다. 또한 페이지네이터 인스턴스를 라우트 또는 컨트롤러 액션에서 반환하면 자동으로 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터가 반환하는 JSON에는 `total`, `current_page`, `last_page` 등과 같은 메타 정보가 포함되어 있습니다. 결과 데이터는 JSON 배열의 `data` 키 하위에 위치합니다. 아래는 라우트에서 페이지네이터 인스턴스를 반환했을 때 생성되는 예시 JSON입니다:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "current_page_url": "http://laravel.app?page=1",
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## 페이지네이션 뷰 커스터마이즈 (Customizing the Pagination View)

기본적으로 페이지네이션 링크를 표시하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. Tailwind를 사용하지 않을 경우, 직접 뷰를 정의해 래퍼의 페이지네이션 링크를 렌더링할 수 있습니다. 페이지네이터 인스턴스의 `links` 메서드의 첫 번째 인수로 뷰 이름을 전달하면 지정한 뷰로 렌더링할 수 있습니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달 예시... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 페이지네이션 뷰를 커스터마이즈하는 가장 쉬운 방법은, `vendor:publish` 명령어로 관련 뷰를 `resources/views/vendor` 디렉터리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어를 실행하면 애플리케이션의 `resources/views/vendor/pagination` 디렉터리에 뷰가 복사됩니다. 이 중 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당하며, 이 파일을 수정해서 페이지네이션 관련 HTML을 바꿀 수 있습니다.

다른 파일을 기본 페이지네이션 뷰로 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `defaultView` 및 `defaultSimpleView` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### Bootstrap 사용

Laravel에는 [Bootstrap CSS](https://getbootstrap.com/) 기반의 페이지네이션 뷰도 포함되어 있습니다. Tailwind 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내부에서 페이지네이터의 `useBootstrapFour`나 `useBootstrapFive` 메서드를 호출하면 됩니다:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                                     | 설명                                                                                      |
| ----------------------------------------- | ---------------------------------------------------------------------------------------- |
| `$paginator->count()`                     | 현재 페이지의 항목 개수 가져오기.                                                         |
| `$paginator->currentPage()`               | 현재 페이지 번호 가져오기.                                                                |
| `$paginator->firstItem()`                 | 결과 중 첫 번째 항목의 번호 가져오기.                                                     |
| `$paginator->getOptions()`                | 페이지네이터 옵션 가져오기.                                                               |
| `$paginator->getUrlRange($start, $end)`   | 페이지네이션 URL 범위 생성.                                                               |
| `$paginator->hasPages()`                  | 여러 페이지로 분할할 만큼 항목이 충분한지 확인.                                           |
| `$paginator->hasMorePages()`              | 데이터 저장소에 더 많은 항목이 있는지 확인.                                               |
| `$paginator->items()`                     | 현재 페이지에 해당하는 항목 가져오기.                                                     |
| `$paginator->lastItem()`                  | 결과 중 마지막 항목의 번호 가져오기.                                                      |
| `$paginator->lastPage()`                  | 마지막으로 접근 가능한 페이지의 번호 가져오기 (`simplePaginate` 사용 시에는 제공되지 않음).|
| `$paginator->nextPageUrl()`               | 다음 페이지에 대한 URL 가져오기.                                                          |
| `$paginator->onFirstPage()`               | 현재 첫 페이지에 있는지 확인.                                                             |
| `$paginator->onLastPage()`                | 현재 마지막 페이지에 있는지 확인.                                                         |
| `$paginator->perPage()`                   | 페이지당 표시할 항목 개수.                                                                |
| `$paginator->previousPageUrl()`           | 이전 페이지에 대한 URL 가져오기.                                                          |
| `$paginator->total()`                     | 데이터 저장소에 일치하는 전체 항목 수 확인 (`simplePaginate` 사용 시에는 제공되지 않음).  |
| `$paginator->url($page)`                  | 특정 페이지 번호에 대한 URL 가져오기.                                                     |
| `$paginator->getPageName()`               | 페이지를 저장할 때 사용하는 쿼리 문자열 변수명 가져오기.                                  |
| `$paginator->setPageName($name)`          | 페이지를 저장할 때 사용하는 쿼리 문자열 변수명 지정.                                      |
| `$paginator->through($callback)`          | 콜백을 활용해 각 항목 변환.                                                              |

</div>

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드

각 커서 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| `$paginator->count()`           | 현재 페이지의 항목 개수 가져오기.                            |
| `$paginator->cursor()`          | 현재 커서 인스턴스 가져오기.                                 |
| `$paginator->getOptions()`      | 페이지네이터 옵션 가져오기.                                  |
| `$paginator->hasPages()`        | 여러 페이지로 분할할 만큼 항목이 충분한지 확인.              |
| `$paginator->hasMorePages()`    | 데이터 저장소에 더 많은 항목이 있는지 확인.                  |
| `$paginator->getCursorName()`   | 커서를 저장할 때 사용하는 쿼리 문자열 변수명 가져오기.       |
| `$paginator->items()`           | 현재 페이지에 해당하는 항목 가져오기.                        |
| `$paginator->nextCursor()`      | 다음 항목 집합에 대한 커서 인스턴스 가져오기.                |
| `$paginator->nextPageUrl()`     | 다음 페이지에 대한 URL 가져오기.                             |
| `$paginator->onFirstPage()`     | 현재 첫 페이지에 있는지 확인.                                |
| `$paginator->onLastPage()`      | 현재 마지막 페이지에 있는지 확인.                            |
| `$paginator->perPage()`         | 페이지당 표시할 항목 개수.                                   |
| `$paginator->previousCursor()`  | 이전 항목 집합에 대한 커서 인스턴스 가져오기.                |
| `$paginator->previousPageUrl()` | 이전 페이지에 대한 URL 가져오기.                             |
| `$paginator->setCursorName()`   | 커서를 저장할 때 사용하는 쿼리 문자열 변수명 지정.           |
| `$paginator->url($cursor)`      | 특정 커서 인스턴스에 대한 URL 가져오기.                      |

</div>
