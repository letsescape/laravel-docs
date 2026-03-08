# 데이터베이스: Query Builder (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크로 처리하기](#chunking-results)
    - [지연 스트리밍으로 결과 처리하기](#streaming-results-lazily)
    - [집계](#aggregates)
- [Select 문](#select-statements)
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
    - [논리 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [Full Text Where 절](#full-text-where-clauses)
    - [벡터 유사도 절](#vector-similarity-clauses)
- [정렬, 그룹화, Limit 및 Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 문](#insert-statements)
    - [Upsert](#upserts)
- [Update 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 Query Builder는 데이터베이스 쿼리를 생성하고 실행하기 위한 편리하고 유연한 인터페이스를 제공합니다. 이 기능을 사용하면 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 동작합니다.

Laravel Query Builder는 PDO 파라미터 바인딩(parameter binding)을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 Query Builder에 전달되는 문자열을 별도로 정리하거나 정제할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조되는 컬럼 이름(예: `order by` 컬럼)을 사용자 입력으로 직접 결정하도록 해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` facade가 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 Query Builder 인스턴스를 반환하며, 이후 다양한 조건을 체이닝하여 추가할 수 있습니다. 마지막으로 `get` 메서드를 사용하여 쿼리 결과를 가져옵니다.

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

`get` 메서드는 쿼리 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각 결과는 PHP의 `stdClass` 객체 인스턴스로 구성됩니다. 따라서 객체의 속성(property)으로 컬럼 값을 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션(Collection)은 데이터를 변환하거나 집계할 때 매우 강력한 다양한 메서드를 제공합니다. 자세한 내용은 [collection 문서](/docs/12.x/collections)를 참고하십시오.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행 / 단일 컬럼 조회하기

데이터베이스 테이블에서 단 하나의 행만 가져오고 싶다면 `DB` facade의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

조건에 맞는 레코드가 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키도록 하려면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 처리되지 않으면 자동으로 404 HTTP 응답이 클라이언트에 반환됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 아니라 단일 값만 필요하다면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 지정한 컬럼의 값을 직접 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼을 기준으로 단일 행을 조회하려면 `find` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

단일 컬럼의 값만 모아서 `Illuminate\Support\Collection` 인스턴스로 받고 싶다면 `pluck` 메서드를 사용할 수 있습니다. 아래 예제에서는 사용자 직함(title) 목록을 가져옵니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인수를 전달하면 결과 컬렉션의 키로 사용할 컬럼을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크로 처리하기

수천 개 이상의 데이터 레코드를 처리해야 하는 경우 `DB` facade가 제공하는 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 작은 단위(청크)로 나누어 가져오고, 각 청크를 클로저로 전달하여 처리할 수 있게 합니다.

예를 들어 `users` 테이블 전체를 한 번에 100개씩 가져올 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리를 중단할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```

청크 처리 중에 데이터베이스 레코드를 업데이트하면 예상치 못한 결과가 발생할 수 있습니다. 이러한 경우에는 `chunkById` 메서드를 사용하는 것이 좋습니다. 이 메서드는 기본 키를 기준으로 자동 페이지네이션을 수행합니다.

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

`chunkById`와 `lazyById` 메서드는 내부적으로 자체 `where` 조건을 추가하기 때문에, 보통 자신의 조건을 클로저로 묶어 [논리 그룹화](#logical-grouping)하는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 때 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 줄 수 있습니다. 이 경우 일부 레코드가 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍으로 결과 처리하기

`lazy` 메서드는 기본적으로 [chunk 메서드](#chunking-results)와 유사하게 동작하며 내부적으로 데이터를 청크 단위로 가져옵니다. 하지만 각 청크를 콜백에 전달하는 대신 `lazy()` 메서드는 `LazyCollection`을 반환합니다. 이를 통해 결과를 하나의 스트림처럼 처리할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

반복 처리 중에 데이터를 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드는 기본 키를 기준으로 자동 페이지네이션을 수행합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 처리 중에 레코드를 업데이트하거나 삭제할 때 기본 키 또는 외래 키가 변경되면 일부 레코드가 결과에서 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 (Aggregates)

Query Builder는 `count`, `max`, `min`, `avg`, `sum`과 같은 다양한 집계 메서드를 제공합니다. 쿼리를 구성한 뒤 이러한 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

다른 조건과 함께 사용할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

조건에 맞는 레코드가 존재하는지 확인할 때 `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```