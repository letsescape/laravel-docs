# 데이터베이스: Query Builder (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 처리](#chunking-results)
    - [지연 스트리밍 결과](#streaming-results-lazily)
    - [집계](#aggregates)
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
    - [Full Text Where 절](#full-text-where-clauses)
    - [벡터 유사도 절](#vector-similarity-clauses)
- [정렬, 그룹화, Limit 및 Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [Upsert](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 구성 요소](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더(Query Builder)는 데이터베이스 쿼리를 생성하고 실행하기 위한 편리하고 유연한 인터페이스를 제공합니다. 애플리케이션에서 수행하는 대부분의 데이터베이스 작업에 사용할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 동작합니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 쿼리 바인딩으로 전달되는 문자열을 별도로 정리(clean)하거나 필터링(sanitize)할 필요가 없습니다.

> [!WARNING]  
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 사용자 입력을 사용하여 쿼리에서 참조되는 컬럼 이름(예: "order by" 컬럼)을 결정하도록 절대 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

`DB` facade가 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 fluent 쿼리 빌더 인스턴스를 반환하며, 여기에 추가 조건을 체이닝하고 마지막에 `get` 메서드를 호출하여 결과를 가져올 수 있습니다.

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

`get` 메서드는 쿼리 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각 결과는 PHP의 `stdClass` 객체 인스턴스이며, 컬럼 값은 객체의 속성으로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]  
> Laravel 컬렉션(Collection)은 데이터를 매핑(mapping)하거나 축소(reduce)할 때 사용할 수 있는 매우 강력한 다양한 메서드를 제공합니다. 자세한 내용은 [컬렉션 문서](/docs/master/collections)를 참고하십시오.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행 / 단일 컬럼 조회

데이터베이스 테이블에서 단일 행만 조회하려면 `DB` facade의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

일치하는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외를 잡지 않으면 자동으로 404 HTTP 응답이 클라이언트에 반환됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고 특정 컬럼 값 하나만 필요하다면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 컬럼 값을 직접 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 단일 행을 조회하려면 `find` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회

하나의 컬럼 값들로 이루어진 `Illuminate\Support\Collection` 인스턴스를 가져오려면 `pluck` 메서드를 사용할 수 있습니다. 아래 예시는 사용자 직함(title) 목록을 가져옵니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수를 사용하면 컬렉션의 키로 사용할 컬럼을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리 (Chunking Results)

수천 개 이상의 데이터 레코드를 처리해야 한다면 `DB` facade의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 작은 단위로 나누어 가져오고 각 청크를 클로저에 전달하여 처리합니다.

예를 들어 `users` 테이블을 100개 레코드씩 처리할 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리가 중단됩니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```

청크 처리 중에 데이터베이스 레코드를 업데이트하는 경우 예상치 못한 결과가 발생할 수 있습니다. 이 경우에는 `chunkById` 메서드를 사용하는 것이 좋습니다. 이 메서드는 기본 키를 기준으로 자동으로 페이지네이션을 수행합니다.

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

`chunkById` 및 `lazyById` 메서드는 자체적으로 `where` 조건을 추가하므로, 일반적으로 사용자 정의 조건은 클로저를 사용하여 [논리적으로 그룹화](#logical-grouping)하는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 때 기본 키 또는 외래 키를 변경하면 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 청크 결과에 포함되지 않을 수 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍 결과 (Streaming Results Lazily)

`lazy` 메서드는 `chunk` 메서드와 유사하게 쿼리를 청크 단위로 실행합니다. 하지만 각 청크를 콜백으로 전달하는 대신 `lazy()` 메서드는 [LazyCollection](/docs/master/collections#lazy-collections)을 반환합니다. 이를 통해 결과를 하나의 스트림처럼 처리할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

반복 처리 중에 데이터를 업데이트할 예정이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드는 기본 키를 기준으로 자동 페이지네이션을 수행합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]  
> 반복 처리 중 레코드를 업데이트하거나 삭제할 때 기본 키 또는 외래 키 변경은 쿼리 결과에 영향을 줄 수 있습니다.

<a name="aggregates"></a>
### 집계 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 집계 값을 가져오는 다양한 메서드를 제공합니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

다른 조건과 함께 사용하여 집계 계산 범위를 조정할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

특정 조건에 맞는 레코드 존재 여부만 확인하려면 `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

(문서의 이후 섹션들도 동일한 방식으로 계속 번역됩니다. 길이 제한으로 인해 여기서 일부만 표시됩니다.)