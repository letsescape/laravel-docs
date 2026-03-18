# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과 청킹](#chunking-results)
    - [지연 결과 스트리밍](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니온](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All / None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전문 검색 Where 절](#full-text-where-clauses)
    - [벡터 유사도 절](#vector-similarity-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [제한 및 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [Upsert](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행하는 데 편리하고 유창한 인터페이스를 제공합니다. 이는 애플리케이션에서 대부분의 데이터베이스 작업을 수행하는 데 사용할 수 있으며 Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

Laravel 쿼리 빌더는 PDO 매개변수 바인딩을 사용하여 SQL 주입 공격으로부터 애플리케이션을 보호합니다. 쿼리 빌더에 쿼리 바인딩으로 전달된 문자열을 정리하거나 정리할 필요가 없습니다.

> [!WARNING]
> PDO는 바인딩 열 이름을 지원하지 않습니다. 따라서 "순서 기준" 열을 포함하여 쿼리에서 참조하는 열 이름을 사용자 입력이 지시하도록 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 조회

쿼리를 시작하기 위해 `DB` 파사드에서 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 주어진 테이블에 대해 유연한 쿼리 빌더 인스턴스를 반환하므로 쿼리에 더 많은 제약 조건을 연결할 수 있으며 마지막으로 `get` 메서드를 사용하여 쿼리의 결과를 검색할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리의 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 여기서 각 결과는 PHP `stdClass` 개체의 인스턴스입니다. 객체의 속성으로 열에 액세스하여 각 열의 값에 액세스할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑 및 축소를 위한 다양하고 강력한 메서드를 제공합니다. Laravel 컬렉션에 대한 자세한 내용은 [컬렉션 문서](/docs/13.x/collections)를 확인하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 / 컬럼 조회

데이터베이스 테이블에서 단일 행만 검색해야 한다면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

데이터베이스 테이블에서 단일 행을 검색하고 싶지만 일치하는 행이 없으면 `Illuminate\Database\RecordNotFoundException`를 발생시키는 경우 `firstOrFail` 메서드를 사용할 수 있습니다. `RecordNotFoundException`가 포착되지 않으면 404 HTTP 응답이 자동으로 클라이언트에 다시 전송됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않은 경우 `value` 메서드를 사용하여 레코드에서 단일 값을 추출할 수 있습니다. 이 메서드는 열의 값을 직접 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 열 값으로 단일 행을 검색하려면 `find` 메서드를 사용합니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회

단일 열의 값을 포함하는 `Illuminate\Support\Collection` 인스턴스를 검색하려면 `pluck` 메서드를 사용할 수 있습니다. 이 예에서는 사용자 직위 컬렉션을 검색합니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인수를 제공하여 결과 컬렉션이 키로 사용해야 하는 열을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청킹

수천 개의 데이터베이스 레코드로 작업해야 하는 경우 `DB` 파사드에서 제공하는 `chunk` 메서드 사용을 고려해보세요. 이 메서드는 한 번에 작은 결과 묶음을 가져와 각 묶음을 클로저에 전달합니다. 예를 들어, 한 번에 100개의 레코드 청크로 전체 `users` 테이블을 검색해 보겠습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하여 추가 청크 처리를 중지할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```

결과를 청크하는 동안 데이터베이스 레코드를 업데이트하는 경우 청크 결과가 예상치 못한 방식으로 변경될 수 있습니다. 청크하는 동안 검색된 레코드를 업데이트하려는 경우 항상 `chunkById` 메서드를 대신 사용하는 것이 가장 좋습니다. 이 메서드는 레코드의 기본 키를 기반으로 결과를 자동으로 페이지 매깁니다.

```php
DB::table('users')->where('active', false)
    ->chunkById(100, function (Collection $users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

`chunkById` 및 `lazyById` 메서드는 실행 중인 쿼리에 자체 "where" 조건을 추가하므로 일반적으로 클로저 내에서 자체 조건을 [논리적으로 그룹화](#logical-grouping)해야 합니다.

```php
DB::table('users')->where(function ($query) {
    $query->where('credits', 1)->orWhere('credits', 2);
})->chunkById(100, function (Collection $users) {
    foreach ($users as $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['credits' => 3]);
    }
});
```

> [!WARNING]
> 청크 콜백 내에서 레코드를 업데이트하거나 삭제할 때 기본 키 또는 외래 키에 대한 변경 사항이 청크 쿼리에 영향을 미칠 수 있습니다. 이로 인해 청크 결과에 레코드가 포함되지 않을 가능성이 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 결과 스트리밍

`lazy` 메서드는 쿼리를 청크로 실행한다는 점에서 [청크 메서드](#chunking-results)와 유사하게 작동합니다. 그러나 각 청크를 콜백에 전달하는 대신 `lazy()` 메서드는 결과를 단일 스트림으로 상호 작용할 수 있는 [LazyCollection](/docs/13.x/collections#lazy-collections)을 반환합니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

다시 한 번, 검색된 레코드를 반복하면서 업데이트하려는 경우 대신 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 좋습니다. 이러한 메서드는 레코드의 기본 키를 기반으로 결과를 자동으로 페이지 매깁니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 레코드를 반복하는 동안 레코드를 업데이트하거나 삭제할 때 기본 키 또는 외래 키에 대한 변경 사항이 청크 쿼리에 영향을 미칠 수 있습니다. 이로 인해 잠재적으로 레코드가 결과에 포함되지 않을 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등의 집계 값을 조회하기 위한 다양한 메서드도 제공합니다. 쿼리를 구성한 후 다음 메서드 중 하나를 호출할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 이러한 메서드를 다른 절과 결합하여 집계 값이 계산되는 방식을 세밀하게 조정할 수 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 확인

`count` 메서드를 사용하여 쿼리의 제약 조건과 일치하는 레코드가 있는지 확인하는 대신 `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Select 구문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 절 지정하기

항상 데이터베이스 테이블에서 모든 열을 선택하고 싶지는 않을 수도 있습니다. `select` 메서드를 사용하면 쿼리에 대한 사용자 지정 "select" 절을 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 쿼리가 고유한 결과를 반환하도록 강제할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고 기존 select 절에 열을 추가하려는 경우 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

때로는 쿼리에 임의의 문자열을 삽입해야 할 수도 있습니다. 원시 문자열 표현식을 생성하려면 `DB` 파사드에서 제공하는 `raw` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> 원시 문은 쿼리에 문자열로 주입되므로 SQL 주입 취약점이 발생하지 않도록 매우 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드를 사용하는 대신 다음 메서드를 사용하여 쿼리의 다양한 부분에 raw 표현식을 삽입할 수도 있습니다. **Laravel은 원시 표현식을 사용하는 쿼리가 SQL 주입 취약점으로부터 보호된다는 점을 보장할 수 없습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 이 메서드는 두 번째 인수로 선택적 바인딩 배열을 받습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드를 사용하여 쿼리에 원시 "where" 절을 삽입할 수 있습니다. 이 메서드는 두 번째 인수로 선택적 바인딩 배열을 허용합니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다. 이 메서드는 두 번째 인수로 선택적 바인딩 배열을 허용합니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더를 사용하여 쿼리에 조인 절을 추가할 수도 있습니다. 기본적인 "내부 조인"을 수행하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용할 수 있습니다. `join` 메서드에 전달된 첫 번째 인수는 조인해야 하는 테이블의 이름이고 나머지 인수는 조인에 대한 열 제약 조건을 지정합니다. 단일 쿼리에서 여러 테이블을 조인할 수도 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 절

"내부 조인" 대신 "왼쪽 ​​조인" 또는 "오른쪽 조인"을 수행하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이러한 메서드는 `join` 메서드와 동일한 서명을 갖습니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### Cross Join 절

`crossJoin` 메서드를 사용하여 "크로스 조인"을 수행할 수 있습니다. 크로스 조인은 첫 번째 테이블과 조인된 테이블 사이에 카르테시안 곱(Cartesian Product)을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

또한 고급 조인 절을 지정할 수도 있습니다. 시작하려면 클로저를 `join` 메서드의 두 번째 인수로 전달하세요. 클로저는 "join" 절에 제약 조건을 지정할 수 있는 `Illuminate\Database\Query\JoinClause` 인스턴스를 수신합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에 "where" 절을 사용하려면 `JoinClause` 인스턴스에서 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 두 컬럼을 비교하는 대신 이 메서드들은 컬럼을 값과 비교합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인

`joinSub`, `leftJoinSub` 및 `rightJoinSub` 메서드를 사용하여 쿼리를 하위 쿼리에 조인할 수 있습니다. 각 메서드는 하위 쿼리, 테이블 별칭, 관련 열을 정의하는 클로저라는 세 가지 인수를 받습니다. 이 예에서는 각 사용자 레코드에 사용자가 가장 최근에 게시한 블로그 게시물의 `created_at` 타임스탬프도 포함되어 있는 사용자 컬렉션을 검색합니다.

```php
$latestPosts = DB::table('posts')
    ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
    ->where('is_published', true)
    ->groupBy('user_id');

$users = DB::table('users')
    ->joinSub($latestPosts, 'latest_posts', function (JoinClause $join) {
        $join->on('users.id', '=', 'latest_posts.user_id');
    })->get();
```

<a name="lateral-joins"></a>
#### Lateral 조인

> [!WARNING]
> Lateral 조인은 현재 PostgreSQL, MySQL >= 8.0.14 및 SQL Server에서 지원됩니다.

하위 쿼리로 "측면 조인"을 수행하려면 `joinLateral` 및 `leftJoinLateral` 메서드를 사용할 수 있습니다. 이러한 각 메서드는 하위 쿼리와 해당 테이블 별칭이라는 두 가지 인수를 받습니다. 조인 조건은 해당 하위 쿼리의 `where` 절 내에 지정되어야 합니다. 측면 조인은 각 행에 대해 평가되며 하위 쿼리 외부의 열을 참조할 수 있습니다.

이 예에서는 사용자 컬렉션과 사용자의 가장 최근 블로그 게시물 3개를 검색합니다. 각 사용자는 결과 집합에서 가장 최근 블로그 게시물당 하나씩 최대 3개의 행을 생성할 수 있습니다. 조인 조건은 현재 사용자 행을 참조하는 하위 쿼리 내의 `whereColumn` 절을 사용하여 지정됩니다.

```php
$latestPosts = DB::table('posts')
    ->select('id as post_id', 'title as post_title', 'created_at as post_created_at')
    ->whereColumn('user_id', 'users.id')
    ->orderBy('created_at', 'desc')
    ->limit(3);

$users = DB::table('users')
    ->joinLateral($latestPosts, 'latest_posts')
    ->get();
```

<a name="unions"></a>
## 유니온 (Unions)

쿼리 빌더는 둘 이상의 쿼리를 함께 "유니온(결합)"하는 편리한 메서드도 제공합니다. 예를 들어 초기 쿼리를 생성하고 `union` 메서드를 사용하여 이를 더 많은 쿼리와 결합할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$usersWithoutFirstName = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($usersWithoutFirstName)
    ->get();
```

`union` 메서드 외에도 쿼리 빌더는 `unionAll` 메서드를 제공합니다. `unionAll`을 사용하여 결합된 쿼리는 중복 결과가 제거되지 않습니다. `unionAll` 메서드는 `union` 메서드와 동일한 시그니처를 갖습니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용하여 쿼리에 "where" 절을 추가할 수 있습니다. `where` 메서드에 대한 가장 기본적인 호출에는 세 가지 인수가 필요합니다. 첫 번째 인수는 열의 이름입니다. 두 번째 인수는 데이터베이스가 지원하는 연산자 중 하나일 수 있는 연산자입니다. 세 번째 인수는 열의 값과 비교할 값입니다.

예를 들어, 다음 쿼리는 `votes` 열의 값이 `100`와 같고 `age` 열의 값이 `35`보다 큰 사용자를 검색합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의상 해당 열이 주어진 값에 대해 `=`인지 확인하려는 경우 해당 값을 `where` 메서드의 두 번째 인수로 전달할 수 있습니다. Laravel은 `=` 연산자를 사용한다고 가정합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

여러 열에 대해 쿼리를 신속하게 처리하기 위해 `where` 메서드에 연관 배열을 제공할 수도 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

이전에 언급한 대로 데이터베이스 시스템에서 지원하는 모든 연산자를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>=', 100)
    ->get();

$users = DB::table('users')
    ->where('votes', '<>', 100)
    ->get();

$users = DB::table('users')
    ->where('name', 'like', 'T%')
    ->get();
```

`where` 함수에 조건 배열을 전달할 수도 있습니다. 배열의 각 요소는 일반적으로 `where` 메서드에 전달되는 세 가지 인수를 포함하는 배열이어야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 바인딩 열 이름을 지원하지 않습니다. 따라서 "순서 기준" 열을 포함하여 쿼리에서 참조하는 열 이름을 사용자 입력이 지시하도록 허용해서는 안 됩니다.

> [!WARNING]
> MySQL 및 MariaDB는 문자열-번호 비교에서 자동으로 문자열을 정수로 타입 변환합니다. 이 과정에서 숫자가 아닌 문자열이 `0`로 변환되어 예상치 못한 결과가 발생할 수 있습니다. 예를 들어 테이블에 값이 `aaa`인 `secret` 열이 있고 `User::where('secret', 0)`를 실행하면 해당 행이 반환됩니다. 이를 방지하려면 쿼리에서 사용하기 전에 모든 값이 적절한 유형으로 변환되었는지 확인하세요.

<a name="or-where-clauses"></a>
### Or Where 절

쿼리 빌더의 `where` 메서드에 대한 호출을 함께 연결할 때 "where" 절은 `and` 연산자를 사용하여 함께 결합됩니다. 그러나 `or` 연산자를 사용하여 절을 쿼리에 조인하려면 `orWhere` 메서드를 사용할 수 있습니다. `orWhere` 메서드는 `where` 메서드와 동일한 인수를 허용합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호 안에 "or" 조건을 그룹화해야 하는 경우 클로저를 `orWhere` 메서드의 첫 번째 인수로 전달할 수 있습니다.

```php
use Illuminate\Database\Query\Builder; 

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
        })
    ->get();
```

위의 예에서는 다음 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 범위가 적용될 때 예기치 않은 동작을 방지하려면 항상 `orWhere` 호출을 그룹화해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 지정된 쿼리 제약 조건 그룹을 무효화하는 데 사용될 수 있습니다. 예를 들어, 다음 쿼리는 재고 정리 중이거나 가격이 10보다 낮은 제품을 제외합니다.

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### Where Any / All / None 절

때로는 동일한 쿼리 제약 조건을 여러 열에 적용해야 할 수도 있습니다. 예를 들어, 주어진 목록의 열이 `LIKE` 주어진 값인 모든 레코드를 검색할 수 있습니다. `whereAny` 방법을 사용하여 이 작업을 수행할 수 있습니다.

```php
$users = DB::table('users')
    ->where('active', true)
    ->whereAny([
        'name',
        'email',
        'phone',
    ], 'like', 'Example%')
    ->get();
```

위의 쿼리는 다음 SQL을 생성합니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

마찬가지로, `whereAll` 메서드는 주어진 모든 열이 주어진 제약 조건과 일치하는 레코드를 검색하는 데 사용될 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위의 쿼리는 다음 SQL을 생성합니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 주어진 열 중 어느 것도 주어진 제약 조건과 일치하지 않는 레코드를 검색하는 데 사용할 수 있습니다.

```php
$albums = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```

위의 쿼리는 다음 SQL을 생성합니다.

```sql
SELECT *
FROM albums
WHERE published = true AND NOT (
    title LIKE '%explicit%' OR
    lyrics LIKE '%explicit%' OR
    tags LIKE '%explicit%'
)
```

<a name="json-where-clauses"></a>
### JSON Where 절

Laravel은 JSON 열 유형에 대한 지원을 제공하는 데이터베이스에서 JSON 열 유형 쿼리도 지원합니다. 현재 여기에는 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+ 및 SQLite 3.39.0+가 포함됩니다. JSON 열을 쿼리하려면 `->` 연산자를 사용하세요.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

쿼리 JSON 배열에 `whereJsonContains` 및 `whereJsonDoesntContain` 방법을 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

애플리케이션이 MariaDB, MySQL 또는 PostgreSQL 데이터베이스를 사용하는 경우 값 배열을 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드에 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한 `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용하여 JSON 키를 포함하거나 포함하지 않는 결과를 검색할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, 길이에 따라 쿼리 JSON 배열에 `whereJsonLength` 방법을 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가적인 Where 절

**어디처럼/또는어디처럼/어디같지 않음/또는어디같지 않음**

`whereLike` 메서드를 사용하면 패턴 일치를 위해 쿼리에 "LIKE" 절을 추가할 수 있습니다. 이러한 방법은 대소문자 구분을 전환하는 기능과 함께 문자열 일치 쿼리를 수행하는 데이터베이스에 구애받지 않는 방법을 제공합니다. 기본적으로 문자열 일치는 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 통해 대소문자 구분 검색을 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드를 사용하면 LIKE 조건과 함께 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드를 사용하면 쿼리에 "NOT LIKE" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로 `orWhereNotLike`를 사용하여 NOT LIKE 조건과 함께 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike` 대/소문자 구분 검색 옵션은 현재 SQL Server에서 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 주어진 열의 값이 주어진 배열 내에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 주어진 열의 값이 주어진 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 메서드의 두 번째 인수로 쿼리 객체를 제공할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위의 예에서는 다음 SQL을 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 대규모 정수 바인딩 배열을 추가하는 경우 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**어디 사이에 / 또는어디 사이에**

`whereBetween` 메서드는 열 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**Between / 또는WhereNotBetween**

`whereNotBetween` 메서드는 열 값이 두 값 외부에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / 또는WhereBetweenColumns / 또는WhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 열 값이 동일한 테이블 행에 있는 두 열의 두 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 열 값이 동일한 테이블 행에 있는 두 열의 두 값 외부에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**사이에 있는 값 / 사이에 없는 값 / 또는 사이에 있는 값 / 또는 사이에 없는 값**

`whereValueBetween` 메서드는 지정된 값이 동일한 테이블 행에 있는 동일한 유형의 두 열 값 사이에 있는지 확인합니다.

```php
$products = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween` 메서드는 값이 동일한 테이블 행에 있는 두 열의 값 외부에 있는지 확인합니다.

```php
$products = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 주어진 열의 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 열의 값이 `NULL`가 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 열의 값을 날짜와 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 열의 값을 특정 월과 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 열의 값을 특정 날짜와 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 열의 값을 특정 연도와 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 열의 값을 특정 시간과 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast` 및 `whereFuture` 메서드는 열의 값이 과거인지 미래인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast` 및 `whereNowOrFuture` 메서드는 열의 값이 현재 날짜와 시간을 포함하여 과거인지 미래인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday` 및 `whereAfterToday` 메서드는 열의 값이 각각 오늘, 오늘 이전 또는 오늘 이후인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereBeforeToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereAfterToday('due_at')
    ->get();
```

마찬가지로 `whereTodayOrBefore` 및 `whereTodayOrAfter` 메서드를 사용하여 열의 값이 오늘 날짜를 포함하여 오늘 이전인지 오늘 이후인지 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / 또는WhereColumn**

`whereColumn` 메서드를 사용하여 두 열이 동일한지 확인할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

`whereColumn` 메서드에 비교 연산자를 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

열 비교 배열을 `whereColumn` 메서드에 전달할 수도 있습니다. 이러한 조건은 `and` 연산자를 사용하여 결합됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

때로는 쿼리의 원하는 논리적 그룹화를 달성하기 위해 괄호 안에 여러 "where" 절을 그룹화해야 할 수도 있습니다. 실제로 예기치 않은 쿼리 동작을 방지하려면 일반적으로 항상 `orWhere` 메서드에 대한 호출을 괄호로 그룹화해야 합니다. 이를 달성하려면 `where` 메서드에 클로저를 전달할 수 있습니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

보시다시피 클로저를 `where` 메서드에 전달하면 쿼리 빌더에 제약 조건 그룹을 시작하도록 지시합니다. 클로저는 괄호 그룹 내에 포함되어야 하는 제약 조건을 설정하는 데 사용할 수 있는 쿼리 빌더 인스턴스를 수신합니다. 위의 예에서는 다음 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 범위가 적용될 때 예기치 않은 동작을 방지하려면 항상 `orWhere` 호출을 그룹화해야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "존재하는 위치" SQL 절을 작성할 수 있습니다. `whereExists` 메서드는 쿼리 빌더 인스턴스를 수신하는 클로저를 허용하므로 "exists" 절 내부에 배치되어야 하는 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 클로저 대신 쿼리 객체를 `whereExists` 메서드에 제공할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위의 두 예제 모두 다음 SQL을 생성합니다.

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 Where 절

때로는 하위 쿼리의 결과를 주어진 값과 비교하는 "where" 절을 구성해야 할 수도 있습니다. `where` 메서드에 클로저와 값을 전달하여 이를 수행할 수 있습니다. 예를 들어, 다음 쿼리는 특정 유형의 최근 "멤버십"을 가진 모든 사용자를 검색합니다.

```php
use App\Models\User;
use Illuminate\Database\Query\Builder;

$users = User::where(function (Builder $query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

또는 하위 쿼리 결과와 열을 비교하는 "where" 절을 구성해야 할 수도 있습니다. 열, 연산자 및 클로저를 `where` 메서드에 전달하여 이를 수행할 수 있습니다. 예를 들어, 다음 쿼리는 금액이 평균보다 적은 모든 소득 기록을 검색합니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색 Where 절

> [!WARNING]
> 절이 현재 MariaDB, MySQL 및 PostgreSQL에서 지원되는 전체 텍스트입니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전체 텍스트 인덱스](/docs/13.x/migrations#available-index-types)가 있는 열의 쿼리에 전체 텍스트 "where" 절을 추가하는 데 사용할 수 있습니다. 이러한 메서드는 Laravel에 의해 기본 데이터베이스 시스템에 적합한 SQL로 변환됩니다. 예를 들어, MariaDB 또는 MySQL을 활용하는 애플리케이션에 대해 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
### 벡터 유사도 절

> [!NOTE]
> 벡터 유사성 절은 현재 `pgvector` 확장을 사용하는 PostgreSQL 연결에서만 지원됩니다. 벡터 열 및 인덱스 정의에 대한 자세한 내용은 [마이그레이션 문서](/docs/13.x/migrations#available-column-types)를 참조하세요.

`whereVectorSimilarTo` 방법은 주어진 벡터에 대한 코사인 유사성을 기준으로 결과를 필터링하고 관련성에 따라 결과를 정렬합니다. `minSimilarity` 임계값은 `0.0`와 `1.0` 사이의 값이어야 합니다. 여기서 `1.0`는 동일합니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

일반 문자열이 벡터 인수로 제공되면 Laravel은 [Laravel AI SDK](/docs/13.x/ai-sdk#embeddings)를 사용하여 자동으로 임베딩을 생성합니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

기본적으로 `whereVectorSimilarTo`는 거리별로 결과를 정렬합니다(가장 유사한 것부터). `false`를 `order` 인수로 전달하여 이 순서를 비활성화할 수 있습니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

더 많은 제어가 필요한 경우 `selectVectorDistance`, `whereVectorDistanceLessThan` 및 `orderByVectorDistance` 메서드를 독립적으로 사용할 수 있습니다.

```php
$documents = DB::table('documents')
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

PostgreSQL를 활용하는 경우 `vector` 열을 생성하기 전에 `pgvector` 확장을 로드해야 합니다.

```php
Schema::ensureVectorExtensionExists();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 및 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 방법을 사용하면 주어진 열을 기준으로 쿼리의 결과를 정렬할 수 있습니다. `orderBy` 메서드에서 허용하는 첫 번째 인수는 정렬하려는 열이어야 하며, 두 번째 인수는 정렬 방향을 결정하며 `asc` 또는 `desc`일 수 있습니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 열을 기준으로 정렬하려면 필요한 만큼 `orderBy`를 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 선택 사항이며 기본적으로 오름차순입니다. 내림차순으로 정렬하려면 `orderBy` 메서드에 대한 두 번째 매개변수를 지정하거나 `orderByDesc`를 사용하면 됩니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

마지막으로 `->` 연산자를 사용하여 결과를 JSON 열 내의 값을 기준으로 정렬할 수 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest` 및 `oldest` 방법을 사용하면 결과를 날짜별로 쉽게 정렬할 수 있습니다. 기본적으로 결과는 테이블의 `created_at` 열을 기준으로 정렬됩니다. 또는 정렬하려는 열 이름을 전달할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 방법은 쿼리 결과를 무작위로 정렬하는 데 사용될 수 있습니다. 예를 들어, 이 메서드를 사용하여 임의의 사용자를 가져올 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 이전에 쿼리에 적용된 "order by" 절을 모두 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

기존의 모든 "order by" 절을 제거하고 완전히 새로운 순서를 쿼리에 적용하기 위해 `reorder` 메서드를 호출할 때 열과 방향을 전달할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

편의를 위해 `reorderDesc` 메서드를 사용하여 쿼리 결과를 내림차순으로 재정렬할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상할 수 있듯이 `groupBy` 및 `having` 메서드를 사용하여 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드의 서명은 `where` 메서드의 서명과 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용하여 지정된 범위 내에서 결과를 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 열로 그룹화하기 위해 `groupBy` 메서드에 여러 인수를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

고급 `having` 문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참조하세요.

<a name="limit-and-offset"></a>
### 제한 및 오프셋

`limit` 및 `offset` 메서드를 사용하여 쿼리에서 반환되는 결과 수를 제한하거나 쿼리에서 지정된 수의 결과를 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

때로는 특정 쿼리 절을 다른 조건에 따라 쿼리에 적용하기를 원할 수도 있습니다. 예를 들어, 들어오는 HTTP 요청에 지정된 입력 값이 있는 경우에만 `where` 문을 적용할 수 있습니다. `when` 방법을 사용하여 이 작업을 수행할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`인 경우에만 지정된 클로저를 실행합니다. 첫 번째 인수가 `false`이면 클로저가 실행되지 않습니다. 따라서 위의 예에서 `when` 메서드에 제공된 클로저는 들어오는 요청에 `role` 필드가 있고 `true`로 평가되는 경우에만 호출됩니다.

`when` 메서드의 세 번째 인수로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 첫 번째 인수가 `false`로 평가되는 경우에만 실행됩니다. 이 기능을 사용하는 방법을 설명하기 위해 이 기능을 사용하여 쿼리의 기본 순서를 구성하겠습니다.

```php
$sortByVotes = $request->boolean('sort_by_votes');

$users = DB::table('users')
    ->when($sortByVotes, function (Builder $query, bool $sortByVotes) {
        $query->orderBy('votes');
    }, function (Builder $query) {
        $query->orderBy('name');
    })
    ->get();
```

<a name="insert-statements"></a>
## Insert 구문 (Insert Statements)

쿼리 빌더는 데이터베이스 테이블에 레코드를 삽입하는 데 사용할 수 있는 `insert` 메서드도 제공합니다. `insert` 메서드는 열 이름과 값의 배열을 허용합니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

배열의 배열을 전달하여 여러 레코드를 한 번에 삽입할 수 있습니다. 각 배열은 테이블에 삽입되어야 하는 레코드를 나타냅니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 데이터베이스에 레코드를 삽입하는 동안 오류를 무시합니다. 이 방법을 사용할 경우 중복 레코드 오류는 무시되며, 데이터베이스 엔진에 따라 다른 유형의 오류도 무시될 수 있다는 점을 유의해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 엄격 모드를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 삽입되어야 하는 데이터를 결정하기 위해 하위 쿼리를 사용하는 동안 테이블에 새 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있는 경우 `insertGetId` 메서드를 사용하여 레코드를 삽입한 다음 ID를 검색합니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL를 사용할 때 `insertGetId` 메서드는 자동 증가 열의 이름이 `id`일 것으로 예상합니다. 다른 "시퀀스"에서 ID를 검색하려면 열 이름을 `insertGetId` 메서드의 두 번째 매개변수로 전달할 수 있습니다.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드를 삽입하고 이미 존재하는 레코드를 사용자가 지정할 수 있는 새 값으로 업데이트합니다. 메서드의 첫 번째 인수는 삽입하거나 업데이트할 값으로 구성되며, 두 번째 인수는 연결된 테이블 내에서 레코드를 고유하게 식별하는 열을 나열합니다. 메서드의 세 번째이자 마지막 인수는 데이터베이스에 일치하는 레코드가 이미 있는 경우 업데이트해야 하는 열 배열입니다.

```php
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```

위의 예에서 Laravel은 두 개의 레코드를 삽입하려고 시도합니다. 동일한 `departure` 및 `destination` 열 값을 가진 레코드가 이미 존재하는 경우 Laravel은 해당 레코드의 `price` 열을 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수 열에 "기본" 또는 "고유" 인덱스가 있어야 합니다. 또한 MariaDB 및 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하고 항상 테이블의 "기본" 및 "고유" 인덱스를 사용하여 기존 레코드를 검색합니다.

<a name="update-statements"></a>
## Update 구문 (Update Statements)

데이터베이스에 레코드를 삽입하는 것 외에도 쿼리 빌더는 `update` 메서드를 사용하여 기존 레코드를 업데이트할 수도 있습니다. `update` 메서드는 `insert` 메서드와 마찬가지로 업데이트할 열을 나타내는 열 및 값 쌍의 배열을 허용합니다. `update` 메서드는 영향을 받은 행 수를 반환합니다. `where` 절을 사용하여 `update` 쿼리를 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

때로는 데이터베이스의 기존 레코드를 업데이트하거나 일치하는 레코드가 없는 경우 이를 생성해야 할 수도 있습니다. 이 시나리오에서는 `updateOrInsert` 메서드를 사용할 수 있습니다. `updateOrInsert` 메서드는 두 개의 인수, 즉 레코드를 찾는 조건의 배열과 업데이트할 열을 나타내는 열 및 값 쌍의 배열을 허용합니다.

`updateOrInsert` 메서드는 첫 번째 인수의 열과 값 쌍을 사용하여 일치하는 데이터베이스 레코드를 찾으려고 시도합니다. 레코드가 존재하는 경우 두 번째 인수의 값으로 업데이트됩니다. 레코드를 찾을 수 없는 경우 두 인수의 병합된 속성을 사용하여 새 레코드가 삽입됩니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

일치하는 레코드의 존재에 따라 데이터베이스에 업데이트되거나 삽입되는 속성을 사용자 지정하기 위해 `updateOrInsert` 메서드에 대한 클로저를 제공할 수 있습니다.

```php
DB::table('users')->updateOrInsert(
    ['user_id' => $user_id],
    fn ($exists) => $exists ? [
        'name' => $data['name'],
        'email' => $data['email'],
    ] : [
        'name' => $data['name'],
        'email' => $data['email'],
        'marketable' => true,
    ],
);
```

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 열을 업데이트할 때 `->` 구문을 사용하여 JSON 개체에서 적절한 키를 업데이트해야 합니다. 이 작업은 MariaDB 10.3+, MySQL 5.7+ 및 PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증감

쿼리 빌더는 지정된 열의 값을 늘리거나 줄이는 편리한 방법도 제공합니다. 이 두 가지 방법 모두 최소한 하나의 인수(수정할 열)를 허용합니다. 열이 증가하거나 감소해야 하는 양을 지정하기 위해 두 번째 인수가 제공될 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요한 경우 증가 또는 감소 작업 중에 업데이트할 추가 열을 지정할 수도 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한 `incrementEach` 및 `decrementEach` 메서드를 사용하여 한 번에 여러 열을 늘리거나 줄일 수 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문 (Delete Statements)

쿼리 빌더의 `delete` 메서드를 사용하여 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 행 수를 반환합니다. `delete` 메서드를 호출하기 전에 "where" 절을 추가하여 `delete` 문을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더에는 `select` 문을 실행할 때 "비관적 잠금"을 달성하는 데 도움이 되는 몇 가지 기능도 포함되어 있습니다. "공유 잠금"이 포함된 명령문을 실행하려면 `sharedLock` 메서드를 호출하면 됩니다. 공유 잠금은 트랜잭션이 커밋될 때까지 선택한 행이 수정되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate` 방법을 사용할 수도 있습니다. "업데이트용" 잠금은 선택한 레코드가 수정되거나 다른 공유 잠금으로 선택되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

필수는 아니지만 [트랜잭션](/docs/13.x/database#database-transactions) 내에서 비관적 잠금을 래핑하는 것이 좋습니다. 이렇게 하면 검색된 데이터가 전체 작업이 완료될 때까지 데이터베이스에서 변경되지 않은 상태로 유지됩니다. 실패할 경우 트랜잭션은 모든 변경 사항을 롤백하고 자동으로 잠금을 해제합니다.

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate()
        ->find(2);

    if ($sender->balance < 100) {
        throw new RuntimeException('Balance too low.');
    }

    DB::table('users')
        ->where('id', $sender->id)
        ->update([
            'balance' => $sender->balance - 100
        ]);

    DB::table('users')
        ->where('id', $receiver->id)
        ->update([
            'balance' => $receiver->balance + 100
        ]);
});
```

<a name="reusable-query-components"></a>
## 재사용 가능한 쿼리 컴포넌트(Reusable Query Components)

애플리케이션 전체에서 쿼리 로직을 반복한 경우 쿼리 빌더의 `tap` 및 `pipe` 메서드를 사용하여 로직을 재사용 가능한 객체로 추출할 수 있습니다. 애플리케이션에 다음 두 가지 쿼리가 있다고 상상해 보세요.

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->orderByDesc('price')
    ->get();

// ...

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

쿼리 간에 공통적인 대상 필터링을 재사용 가능한 객체로 추출하고 싶을 수도 있습니다.

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Query\Builder;

class DestinationFilter
{
    public function __construct(
        private ?string $destination,
    ) {
        //
    }

    public function __invoke(Builder $query): void
    {
        $query->when($this->destination, function (Builder $query) {
            $query->where('destination', $this->destination);
        });
    }
}
```

그런 다음 쿼리 빌더의 `tap` 메서드를 사용하여 객체의 논리를 쿼리에 적용할 수 있습니다.

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

<a name="query-pipes"></a>
#### 쿼리 파이프

`tap` 메서드는 항상 쿼리 빌더를 반환합니다. 쿼리를 실행하고 다른 값을 반환하는 객체를 추출하려면 대신 `pipe` 메서드를 사용할 수 있습니다.

애플리케이션 전체에서 사용되는 공유 [페이지 매기기](/docs/13.x/pagination) 논리를 포함하는 다음 쿼리 개체를 고려하세요. 쿼리 조건을 쿼리에 적용하는 `DestinationFilter`와 달리, `Paginate` 객체는 쿼리를 실행하고 페이지네이터 인스턴스를 반환합니다.

```php
<?php

namespace App\Scopes;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Query\Builder;

class Paginate
{
    public function __construct(
        private string $sortBy = 'timestamp',
        private string $sortDirection = 'desc',
        private int $perPage = 25,
    ) {
        //
    }

    public function __invoke(Builder $query): LengthAwarePaginator
    {
        return $query->orderBy($this->sortBy, $this->sortDirection)
            ->paginate($this->perPage, pageName: 'p');
    }
}
```

쿼리 빌더의 `pipe` 메서드를 사용하면 이 객체를 활용하여 공유 페이지 매김 논리를 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

현재 쿼리 바인딩 및 SQL을 덤프하기 위해 쿼리를 빌드하는 동안 `dd` 및 `dump` 메서드를 사용할 수 있습니다. `dd` 메서드는 디버그 정보를 표시한 다음 요청 실행을 중지합니다. `dump` 메서드는 디버그 정보를 표시하지만 요청이 계속 실행되도록 허용합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드는 쿼리에서 호출되어 모든 매개변수 바인딩이 적절하게 대체된 쿼리의 SQL을 덤프할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
