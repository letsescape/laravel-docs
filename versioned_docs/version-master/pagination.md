# 데이터베이스: 페이지네이션 (Database: Pagination)

- [소개](#introduction)
- [기본 사용법](#basic-usage)
    - [쿼리 빌더 결과 페이지네이션](#paginating-query-builder-results)
    - [Eloquent 결과 페이지네이션](#paginating-eloquent-results)
    - [커서 페이지네이션](#cursor-pagination)
    - [페이지네이터 수동 생성](#manually-creating-a-paginator)
    - [페이지네이션 URL 커스텀](#customizing-pagination-urls)
- [페이지네이션 결과 표시](#displaying-pagination-results)
    - [페이지네이션 링크 윈도우 조정](#adjusting-the-pagination-link-window)
    - [결과를 JSON으로 변환](#converting-results-to-json)
- [페이지네이션 뷰 커스텀](#customizing-the-pagination-view)
    - [Bootstrap 사용](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [CursorPaginator 인스턴스 메서드](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개 (Introduction)

다른 프레임워크에서는 페이지네이션이 매우 번거로울 수 있습니다. Laravel의 페이지네이션 방식이 여러분에게 새로운 경험이 되기를 기대합니다. Laravel의 페이지네이터는 [쿼리 빌더](/docs/master/queries)와 [Eloquent ORM](/docs/master/eloquent)에 통합되어 있어, 별도의 설정 없이도 데이터베이스 레코드를 손쉽게 페이지네이션할 수 있도록 지원합니다.

기본적으로, 페이지네이터가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com/)와 호환되도록 설계되어 있습니다. 또한, Bootstrap용 페이지네이션 뷰도 지원합니다.

<a name="tailwind"></a>
#### Tailwind

Laravel의 기본 Tailwind 페이지네이션 뷰를 Tailwind 4.x와 함께 사용할 경우, 애플리케이션의 `resources/css/app.css` 파일이 이미 Laravel 페이지네이션 뷰에 맞게 다음과 같이 적절하게 구성되어 있을 것입니다:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션

항목을 페이지네이션하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/master/queries)나 [Eloquent 쿼리](/docs/master/eloquent)에 있는 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지에 따라 쿼리의 "limit"과 "offset"을 자동으로 처리합니다. 기본적으로 현재 페이지는 HTTP 요청의 쿼리 문자열 인수인 `page`의 값으로 감지됩니다. 이 값은 Laravel이 자동으로 감지하며, 페이지네이터가 생성하는 링크에도 자동으로 삽입됩니다.

아래 예제에서는 `paginate` 메서드에 "한 페이지당 보여주고 싶은 항목 수"만 인수로 전달하고 있습니다. 여기서는 한 페이지에 `15`개의 항목을 표시하도록 지정합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 모든 애플리케이션 사용자를 표시합니다.
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
#### 단순 페이지네이션

`paginate` 메서드는 쿼리로 매칭된 전체 레코드 수를 계산한 후, 해당 레코드를 데이터베이스에서 가져옵니다. 이렇게 하면 페이지네이터가 전체 페이지 수를 알 수 있습니다. 하지만, 애플리케이션의 UI에서 전체 페이지 수를 표시할 계획이 없다면 이 레코드 카운트 쿼리는 불필요합니다.

따라서 만약 UI에 "다음"과 "이전" 링크만 표시하면 충분하다면, 더 효율적으로 하나의 쿼리만 실행하는 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지네이션

[Eloquent](/docs/master/eloquent) 쿼리도 동일하게 페이지네이션할 수 있습니다. 아래 예제에서는 `App\Models\User` 모델을 15개씩 페이지네이션합니다. 쿼리 빌더 페이지네이션과 거의 동일한 문법임을 알 수 있습니다:

```php
use App\Models\User;

$users = User::paginate(15);
```

물론, `where` 절 등 다른 쿼리 조건들을 지정한 후에도 `paginate` 메서드를 호출할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent 모델을 페이지네이션할 때도 마찬가지로 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

비슷하게, Eloquent 모델에 대해 `cursorPaginate` 메서드로 커서 페이지네이션도 할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### 한 페이지에서 여러 개의 페이지네이터 인스턴스 사용

애플리케이션에서 하나의 화면에 두 개의 서로 다른 페이지네이터를 보여줘야 할 때가 있습니다. 하지만 두 페이지네이터 모두 현재 페이지를 `page` 쿼리 문자열 파라미터에 저장하면 충돌이 발생합니다. 이 문제를 해결하려면, `paginate`, `simplePaginate`, `cursorPaginate` 메서드에 제공되는 세 번째 인수로 원하는 쿼리 문자열 파라미터 이름을 전달해 페이지네이터별로 현재 페이지를 따로 저장할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate` 및 `simplePaginate`는 SQL의 "offset" 절을 사용하여 쿼리를 생성하는 반면, 커서 페이지네이션은 정렬된 컬럼의 값을 비교하는 "where" 절을 생성하여 데이터의 위치를 지정합니다. 이 방식은 Laravel의 모든 페이지네이션 방식 중에서 가장 효율적인 데이터베이스 성능을 제공합니다. 커서 페이지네이션은 특히 대용량 데이터셋과 "무한 스크롤" UI에 매우 적합합니다.

오프셋 기반 페이지네이션은 페이지 번호가 URL 쿼리 문자열에 포함되어 있지만, 커서 기반 페이지네이션은 쿼리 문자열에 "커서(cursor)" 문자열을 포함합니다. 커서는 다음으로 페이지네이션할 위치와 방향을 포함하는 인코딩된 문자열입니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

쿼리 빌더의 `cursorPaginate` 메서드를 사용해 커서 기반 페이지네이터 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

커서 페이지네이터 인스턴스를 얻으면, `paginate` 및 `simplePaginate` 방식과 동일하게 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터에서 제공하는 인스턴스 메서드에 대한 더 자세한 정보는 [CursorPaginator 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참고하세요.

> [!WARNING]
> 커서 페이지네이션을 사용하려면 쿼리에 반드시 "order by" 절이 포함되어야 합니다. 또한 정렬에 사용된 컬럼들은 반드시 페이지네이션할 테이블의 컬럼이어야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 페이지네이션 vs. 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 예시 SQL 쿼리로 살펴보겠습니다. 아래 두 쿼리는 모두 `users` 테이블을 `id` 기준 오름차순 정렬 후 "두 번째 페이지"를 표시합니다:

```sql
# 오프셋 페이지네이션...
select * from users order by id asc limit 15 offset 15;

# 커서 페이지네이션...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이지네이션 쿼리는 오프셋 페이지네이션과 비교해 다음과 같은 장점이 있습니다:

- 대용량 데이터셋에서 "order by" 컬럼에 인덱스가 있을 경우, 커서 페이지네이션이 더 나은 성능을 보입니다. 오프셋 페이지네이션의 "offset" 절은 앞서 매칭된 모든 데이터를 탐색해야 하기 때문입니다.
- 잦은 데이터 변경(삭제/추가)이 일어나는 데이터셋에서는, 오프셋 페이지네이션이 최근에 추가되거나 삭제된 데이터를 정확하게 반영하지 못해 레코드를 건너뛰거나 중복될 수 있습니다.

반면, 커서 페이지네이션은 다음과 같은 한계가 있습니다:

- `simplePaginate`와 마찬가지로, 커서 페이지네이션은 "다음" 및 "이전" 링크만 표시할 수 있으며, 페이지 번호 링크는 지원하지 않습니다.
- 적어도 하나의 고유 컬럼 또는 컬럼 조합을 기준으로 정렬해야 합니다. `null` 값을 가진 컬럼은 지원하지 않습니다.
- "order by" 절에 쿼리 식별자를 사용할 경우, 반드시 별칭을 지정해 "select" 절에도 포함해야 합니다.
- 파라미터가 포함된 쿼리 식별자는 지원하지 않습니다.

<a name="manually-creating-a-paginator"></a>
### 페이지네이터 수동 생성

때때로, 이미 메모리 내에 존재하는 항목 배열로 직접 페이지네이터 인스턴스를 생성하고 싶을 수 있습니다. 이런 경우 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator`, `Illuminate\Pagination\CursorPaginator` 인스턴스를 직접 만들 수 있습니다.

`Paginator`와 `CursorPaginator` 클래스는 결과 전체 항목 수를 알 필요가 없습니다. 반면, 해당 정보가 필요 없기 때문에 마지막 페이지의 인덱스를 가져오는 메서드는 제공되지 않습니다. `LengthAwarePaginator`는 거의 동일한 인수를 받지만, 결과 집합의 전체 항목 수를 반드시 넘겨주어야 합니다.

즉, `Paginator`는 쿼리 빌더의 `simplePaginate`에, `CursorPaginator`는 `cursorPaginate`에, `LengthAwarePaginator`는 `paginate`에 각각 대응됩니다.

> [!WARNING]
> 페이지네이터 인스턴스를 수동으로 생성할 때는, 결과 배열을 직접 "슬라이스(slice)"해서 넘겨야 합니다. 방법이 익숙하지 않다면 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 참고하세요.

<a name="customizing-pagination-urls"></a>
### 페이지네이션 URL 커스텀

기본적으로 페이지네이터가 생성하는 링크는 현재 요청의 URI를 따릅니다. 그러나 페이지네이터의 `withPath` 메서드를 사용하면, 링크 생성에 사용되는 URI를 원하는 값으로 커스텀할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N` 형식의 링크를 생성하길 원한다면, `withPath` 메서드에 `/admin/users`를 전달하세요:

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

페이지네이션 링크의 쿼리 문자열에 값을 추가하려면, `appends` 메서드를 사용합니다. 예를 들어, 모든 페이지네이션 링크에 `sort=votes`를 추가하고 싶다면, 다음과 같이 `appends`를 호출하세요:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

현재 요청 쿼리 문자열의 모든 값을 페이지네이션 링크에 추가하고 싶다면, `withQueryString` 메서드를 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### 해시 프래그먼트 추가

페이지네이터로 생성된 URL 끝에 "해시 프래그먼트"를 추가해야 할 경우, `fragment` 메서드를 사용하세요. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 붙이고자 한다면 다음과 같이 하면 됩니다:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시 (Displaying Pagination Results)

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를, `simplePaginate`는 `Illuminate\Pagination\Paginator` 인스턴스를, `cursorPaginate`는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 집합에 대한 여러 메서드를 제공합니다. 또한 페이지네이터 인스턴스는 반복 가능한(iterable) 객체이기 때문에 배열처럼 루프를 돌릴 수 있습니다. 즉, 결과를 조회하여 [Blade](/docs/master/blade)로 결과를 출력하고 페이지 링크도 같이 표시할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` 메서드는 결과 집합의 나머지 페이지로 이동하는 링크들을 렌더링합니다. 각각의 링크는 적절한 `page` 쿼리 문자열 변수를 이미 포함하고 있습니다. 참고로, `links` 메서드로 생성되는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환 가능합니다.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지네이션 링크 윈도우 조정

페이지네이터는 페이지 링크를 표시할 때, 현재 페이지 주변의 앞뒤 3페이지도 함께 보여줍니다. `onEachSide` 메서드를 사용하면, 현재 페이지를 중심으로 양쪽에 표시되는 추가 링크 수를 원하는 만큼 조정할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환

Laravel 페이지네이터 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스를 구현하며, `toJson` 메서드를 제공합니다. 따라서 페이지네이션 결과를 JSON으로 손쉽게 변환할 수 있습니다. 경로나 컨트롤러에서 페이지네이터 인스턴스를 바로 반환하면 자동으로 JSON으로 변환됩니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

페이지네이터에서 생성된 JSON은 `total`, `current_page`, `last_page` 등과 같은 메타 정보를 포함합니다. 결과 레코드들은 JSON array의 `data` 키 아래에 있습니다. 아래는 경로에서 페이지네이터 인스턴스를 반환할 때 생성되는 JSON 예시입니다:

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
## 페이지네이션 뷰 커스텀 (Customizing the Pagination View)

기본적으로 페이지네이션 링크를 렌더링하는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. 하지만 Tailwind를 사용하지 않는다면, 직접 만든 뷰로 링크를 렌더링할 수도 있습니다. 페이지네이터 인스턴스에서 `links` 메서드 호출 시, 첫 번째 인수로 사용할 뷰 이름을 넘기면 됩니다:

```blade
{{ $paginator->links('view.name') }}

<!-- 뷰에 추가 데이터 전달... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

하지만 페이지네이션 뷰를 커스텀하는 가장 쉬운 방법은, `vendor:publish` 명령어를 사용해 뷰 파일을 `resources/views/vendor` 디렉터리로 복사하는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

이 명령어를 실행하면 애플리케이션의 `resources/views/vendor/pagination` 디렉터리에 뷰 파일이 생성됩니다. 이 안에 있는 `tailwind.blade.php` 파일이 기본 페이지네이션 뷰에 해당합니다. 이 파일을 수정해 페이지네이션 HTML을 자유롭게 변경할 수 있습니다.

만약 다른 파일을 기본 페이지네이션 뷰로 지정하고 싶다면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 페이지네이터의 `defaultView`와 `defaultSimpleView` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)를 사용하는 페이지네이션 뷰도 내장하고 있습니다. 기본 Tailwind 뷰 대신 Bootstrap 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 페이지네이터의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출하세요:

```php
use Illuminate\Pagination\Paginator;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator 인스턴스 메서드

각 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                                   | 설명                                                                                         |
| --------------------------------------- | --------------------------------------------------------------------------------------------- |
| `$paginator->count()`                   | 현재 페이지의 항목 개수를 가져옵니다.                                                         |
| `$paginator->currentPage()`             | 현재 페이지 번호를 가져옵니다.                                                                |
| `$paginator->firstItem()`               | 결과 중 첫 번째 항목의 번호를 가져옵니다.                                                      |
| `$paginator->getOptions()`              | 페이지네이터의 옵션을 가져옵니다.                                                             |
| `$paginator->getUrlRange($start, $end)` | 지정한 범위의 페이지네이션 URL을 생성합니다.                                                   |
| `$paginator->hasPages()`                | 여러 페이지로 분할할 수 있을 만큼의 항목이 있는지 확인합니다.                                 |
| `$paginator->hasMorePages()`            | 데이터 저장소에 더 많은 항목이 있는지 확인합니다.                                             |
| `$paginator->items()`                   | 현재 페이지의 항목들을 가져옵니다.                                                            |
| `$paginator->lastItem()`                | 결과 중 마지막 항목의 번호를 가져옵니다.                                                      |
| `$paginator->lastPage()`                | 마지막 사용할 수 있는 페이지 번호를 가져옵니다. (`simplePaginate` 사용 시에는 제공되지 않음)  |
| `$paginator->nextPageUrl()`             | 다음 페이지의 URL을 가져옵니다.                                                               |
| `$paginator->onFirstPage()`             | 현재 페이지가 첫 번째 페이지인지 확인합니다.                                                   |
| `$paginator->onLastPage()`              | 현재 페이지가 마지막 페이지인지 확인합니다.                                                    |
| `$paginator->perPage()`                 | 페이지당 표시할 항목 수를 반환합니다.                                                         |
| `$paginator->previousPageUrl()`         | 이전 페이지의 URL을 가져옵니다.                                                               |
| `$paginator->total()`                   | 데이터 저장소에서 일치하는 전체 항목 수를 가져옵니다. (`simplePaginate` 사용 시에는 제공되지 않음) |
| `$paginator->url($page)`                | 지정한 페이지 번호의 URL을 가져옵니다.                                                        |
| `$paginator->getPageName()`             | 페이지를 저장하는 데 사용되는 쿼리 문자열 변수명을 가져옵니다.                                |
| `$paginator->setPageName($name)`        | 페이지를 저장하는 데 사용되는 쿼리 문자열 변수명을 설정합니다.                                |
| `$paginator->through($callback)`        | 콜백을 통해 각 항목을 변환합니다.                                                             |

</div>

<a name="cursor-paginator-instance-methods"></a>
## CursorPaginator 인스턴스 메서드 (Cursor Paginator Instance Methods)

각 커서 페이지네이터 인스턴스는 다음과 같은 메서드를 통해 추가적인 페이지네이션 정보를 제공합니다:

<div class="overflow-auto">

| 메서드                          | 설명                                                                |
| ------------------------------- | -------------------------------------------------------------------- |
| `$paginator->count()`           | 현재 페이지의 항목 수를 가져옵니다.                                  |
| `$paginator->cursor()`          | 현재 커서 인스턴스를 가져옵니다.                                     |
| `$paginator->getOptions()`      | 페이지네이터의 옵션을 가져옵니다.                                    |
| `$paginator->hasPages()`        | 여러 페이지로 분할할 만큼 항목이 있는지 확인합니다.                  |
| `$paginator->hasMorePages()`    | 데이터 저장소에 더 많은 항목이 있는지 확인합니다.                    |
| `$paginator->getCursorName()`   | 커서를 저장하는 데 사용되는 쿼리 문자열 변수명을 가져옵니다.         |
| `$paginator->items()`           | 현재 페이지의 항목을 가져옵니다.                                     |
| `$paginator->nextCursor()`      | 다음 항목 집합을 위한 커서 인스턴스를 가져옵니다.                    |
| `$paginator->nextPageUrl()`     | 다음 페이지의 URL을 가져옵니다.                                      |
| `$paginator->onFirstPage()`     | 현재 페이지가 첫 번째 페이지인지 확인합니다.                          |
| `$paginator->onLastPage()`      | 현재 페이지가 마지막 페이지인지 확인합니다.                           |
| `$paginator->perPage()`         | 페이지당 표시할 항목 수를 반환합니다.                                |
| `$paginator->previousCursor()`  | 이전 항목 집합을 위한 커서 인스턴스를 가져옵니다.                    |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL을 가져옵니다.                                      |
| `$paginator->setCursorName()`   | 커서를 저장하는 데 사용되는 쿼리 문자열 변수명을 설정합니다.          |
| `$paginator->url($cursor)`      | 지정한 커서 인스턴스의 URL을 가져옵니다.                             |

</div>
