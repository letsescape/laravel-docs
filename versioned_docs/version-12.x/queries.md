<!-- # Database: Query Builder -->
# Database: Query Builder

- [Introduction](#introduction)
- [Running Database Queries](#running-database-queries)
    - [Chunking Results](#chunking-results)
    - [Streaming Results Lazily](#streaming-results-lazily)
    - [Aggregates](#aggregates)
- [Select Statements](#select-statements)
- [Raw Expressions](#raw-expressions)
- [Joins](#joins)
- [Unions](#unions)
- [Basic Where Clauses](#basic-where-clauses)
    - [Where Clauses](#where-clauses)
    - [Or Where Clauses](#or-where-clauses)
    - [Where Not Clauses](#where-not-clauses)
    - [Where Any / All / None Clauses](#where-any-all-none-clauses)
    - [JSON Where Clauses](#json-where-clauses)
    - [Additional Where Clauses](#additional-where-clauses)
    - [Logical Grouping](#logical-grouping)
- [Advanced Where Clauses](#advanced-where-clauses)
    - [Where Exists Clauses](#where-exists-clauses)
    - [Subquery Where Clauses](#subquery-where-clauses)
    - [Full Text Where Clauses](#full-text-where-clauses)
    - [Vector Similarity Clauses](#vector-similarity-clauses)
- [Ordering, Grouping, Limit and Offset](#ordering-grouping-limit-and-offset)
    - [Ordering](#ordering)
    - [Grouping](#grouping)
    - [Limit and Offset](#limit-and-offset)
- [Conditional Clauses](#conditional-clauses)
- [Insert Statements](#insert-statements)
    - [Upserts](#upserts)
- [Update Statements](#update-statements)
    - [Updating JSON Columns](#updating-json-columns)
    - [Increment and Decrement](#increment-and-decrement)
- [Delete Statements](#delete-statements)
- [Pessimistic Locking](#pessimistic-locking)
- [Reusable Query Components](#reusable-query-components)
- [Debugging](#debugging)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's database query builder provides a convenient, fluent interface to creating and running database queries. It can be used to perform most database operations in your application and works perfectly with all of Laravel's supported database systems. -->
Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행하는 데 편리하고 유창한 인터페이스를 제공합니다. 이는 애플리케이션에서 대부분의 데이터베이스 작업을 수행하는 데 사용할 수 있으며 Laravel가 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

<!-- The Laravel query builder uses PDO parameter binding to protect your application against SQL injection attacks. There is no need to clean or sanitize strings passed to the query builder as query bindings. -->
Laravel 쿼리 빌더는 PDO 매개변수 바인딩을 사용하여 SQL 주입 공격으로부터 애플리케이션을 보호합니다. 쿼리 빌더에 쿼리 바인딩으로 전달된 문자열을 정리하거나 정리할 필요가 없습니다.

> [!WARNING]
> PDO는 바인딩 열 이름을 지원하지 않습니다. 따라서 "순서 기준" 열을 포함하여 쿼리에서 참조하는 열 이름을 사용자 입력이 지시하도록 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
<!-- ## Running Database Queries -->
## Running Database Queries

<a name="retrieving-all-rows-from-a-table"></a>
<!-- #### Retrieving All Rows From a Table -->
#### Retrieving All Rows From a Table

<!-- You may use the `table` method provided by the `DB` facade to begin a query. The `table` method returns a fluent query builder instance for the given table, allowing you to chain more constraints onto the query and then finally retrieve the results of the query using the `get` method: -->
쿼리를 시작하기 위해 `DB` 파사드에서 제공하는 `table` 메소드를 사용할 수 있습니다. `table` 메소드는 주어진 테이블에 대해 유연한 쿼리 빌더 인스턴스를 반환하므로 쿼리에 더 많은 제약 조건을 연결할 수 있으며 마지막으로 `get` 메소드를 사용하여 쿼리의 결과를 검색할 수 있습니다.

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

<!-- The `get` method returns an `Illuminate\Support\Collection` instance containing the results of the query where each result is an instance of the PHP `stdClass` object. You may access each column's value by accessing the column as a property of the object: -->
`get` 메소드는 쿼리의 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 여기서 각 결과는 PHP `stdClass` 개체의 인스턴스입니다. 객체의 속성으로 열에 액세스하여 각 열의 값에 액세스할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑 및 축소를 위한 다양하고 매우 강력한 방법을 제공합니다. Laravel 컬렉션에 대한 자세한 내용은 [collection documentation](/docs/12.x/collections)를 확인하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
<!-- #### Retrieving a Single Row / Column From a Table -->
#### Retrieving a Single Row / Column From a Table

<!-- If you just need to retrieve a single row from a database table, you may use the `DB` facade's `first` method. This method will return a single `stdClass` object: -->
데이터베이스 테이블에서 단일 행만 검색해야 한다면 `DB` 파사드의 `first` 메소드를 사용할 수 있습니다. 이 메소드는 단일 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

<!-- If you would like to retrieve a single row from a database table, but throw an `Illuminate\Database\RecordNotFoundException` if no matching row is found, you may use the `firstOrFail` method. If the `RecordNotFoundException` is not caught, a 404 HTTP response is automatically sent back to the client: -->
데이터베이스 테이블에서 단일 행을 검색하고 싶지만 일치하는 행이 없으면 `Illuminate\Database\RecordNotFoundException`를 발생시키는 경우 `firstOrFail` 메소드를 사용할 수 있습니다. `RecordNotFoundException`가 포착되지 않으면 404 HTTP 응답이 자동으로 클라이언트에 다시 전송됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

<!-- If you don't need an entire row, you may extract a single value from a record using the `value` method. This method will return the value of the column directly: -->
전체 행이 필요하지 않은 경우 `value` 메서드를 사용하여 레코드에서 단일 값을 추출할 수 있습니다. 이 메소드는 열의 값을 직접 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

<!-- To retrieve a single row by its `id` column value, use the `find` method: -->
`id` 열 값으로 단일 행을 검색하려면 `find` 메서드를 사용합니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
<!-- #### Retrieving a List of Column Values -->
#### Retrieving a List of Column Values

<!-- If you would like to retrieve an `Illuminate\Support\Collection` instance containing the values of a single column, you may use the `pluck` method. In this example, we'll retrieve a collection of user titles: -->
단일 열의 값을 포함하는 `Illuminate\Support\Collection` 인스턴스를 검색하려면 `pluck` 메서드를 사용할 수 있습니다. 이 예에서는 사용자 직위 컬렉션을 검색합니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

<!-- You may specify the column that the resulting collection should use as its keys by providing a second argument to the `pluck` method: -->
`pluck` 메소드에 두 번째 인수를 제공하여 결과 컬렉션이 키로 사용해야 하는 열을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
<!-- ### Chunking Results -->
### Chunking Results

<!-- If you need to work with thousands of database records, consider using the `chunk` method provided by the `DB` facade. This method retrieves a small chunk of results at a time and feeds each chunk into a closure for processing. For example, let's retrieve the entire `users` table in chunks of 100 records at a time: -->
수천 개의 데이터베이스 레코드로 작업해야 하는 경우 `DB` 파사드에서 제공하는 `chunk` 메서드 사용을 고려해보세요. 이 방법은 한 번에 작은 결과 덩어리를 검색하고 처리를 위해 각 덩어리를 클로저에 공급합니다. 예를 들어, 한 번에 100개의 레코드 청크로 전체 `users` 테이블을 검색해 보겠습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

<!-- You may stop further chunks from being processed by returning `false` from the closure: -->
클로저에서 `false`를 반환하여 추가 청크 처리를 중지할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```

<!-- If you are updating database records while chunking results, your chunk results could change in unexpected ways. If you plan to update the retrieved records while chunking, it is always best to use the `chunkById` method instead. This method will automatically paginate the results based on the record's primary key: -->
결과를 청크하는 동안 데이터베이스 레코드를 업데이트하는 경우 청크 결과가 예상치 못한 방식으로 변경될 수 있습니다. 청크하는 동안 검색된 레코드를 업데이트하려는 경우 항상 `chunkById` 메서드를 대신 사용하는 것이 가장 좋습니다. 이 메소드는 레코드의 기본 키를 기반으로 결과를 자동으로 페이지 매깁니다.

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

<!-- Since the `chunkById` and `lazyById` methods add their own "where" conditions to the query being executed, you should typically [logically group](#logical-grouping) your own conditions within a closure: -->
`chunkById` 및 `lazyById` 메소드는 실행 중인 쿼리에 자체 "where" 조건을 추가하므로 일반적으로 클로저 내에서 자체 조건을 [logically group](#logical-grouping)해야 합니다.

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
<!-- ### Streaming Results Lazily -->
### Streaming Results Lazily

<!-- The `lazy` method works similarly to [the chunk method](#chunking-results) in the sense that it executes the query in chunks. However, instead of passing each chunk into a callback, the `lazy()` method returns a [LazyCollection](/docs/12.x/collections#lazy-collections), which lets you interact with the results as a single stream: -->
`lazy` 메서드는 쿼리를 청크로 실행한다는 점에서 [the chunk method](#chunking-results)와 유사하게 작동합니다. 그러나 각 청크를 콜백에 전달하는 대신 `lazy()` 메서드는 결과를 단일 스트림으로 상호 작용할 수 있는 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환합니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

<!-- Once again, if you plan to update the retrieved records while iterating over them, it is best to use the `lazyById` or `lazyByIdDesc` methods instead. These methods will automatically paginate the results based on the record's primary key: -->
다시 한 번, 검색된 레코드를 반복하면서 업데이트하려는 경우 대신 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 좋습니다. 이러한 메소드는 레코드의 기본 키를 기반으로 결과를 자동으로 페이지 매깁니다.

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
<!-- ### Aggregates -->
### Aggregates

<!-- The query builder also provides a variety of methods for retrieving aggregate values like `count`, `max`, `min`, `avg`, and `sum`. You may call any of these methods after constructing your query: -->
쿼리 빌더는 `count`, `max`, `min`, `avg` 및 `sum`와 같은 집계 값을 검색하기 위한 다양한 방법도 제공합니다. 쿼리를 구성한 후 다음 메소드 중 하나를 호출할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

<!-- Of course, you may combine these methods with other clauses to fine-tune how your aggregate value is calculated: -->
물론, 이러한 방법을 다른 절과 결합하여 집계 값이 계산되는 방식을 세부적으로 조정할 수 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
<!-- #### Determining if Records Exist -->
#### Determining if Records Exist

<!-- Instead of using the `count` method to determine if any records exist that match your query's constraints, you may use the `exists` and `doesntExist` methods: -->
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
<!-- ## Select Statements -->
## Select Statements

<a name="specifying-a-select-clause"></a>
<!-- #### Specifying a Select Clause -->
#### Specifying a Select Clause

<!-- You may not always want to select all columns from a database table. Using the `select` method, you can specify a custom "select" clause for the query: -->
항상 데이터베이스 테이블에서 모든 열을 선택하고 싶지는 않을 수도 있습니다. `select` 메소드를 사용하면 쿼리에 대한 사용자 지정 "select" 절을 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

<!-- The `distinct` method allows you to force the query to return distinct results: -->
`distinct` 메서드를 사용하면 쿼리가 고유한 결과를 반환하도록 강제할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

<!-- If you already have a query builder instance and you wish to add a column to its existing select clause, you may use the `addSelect` method: -->
이미 쿼리 빌더 인스턴스가 있고 기존 select 절에 열을 추가하려는 경우 `addSelect` 메소드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
<!-- ## Raw Expressions -->
## Raw Expressions

<!-- Sometimes you may need to insert an arbitrary string into a query. To create a raw string expression, you may use the `raw` method provided by the `DB` facade: -->
때로는 쿼리에 임의의 문자열을 삽입해야 할 수도 있습니다. 원시 문자열 표현식을 생성하려면 `DB` 파사드에서 제공하는 `raw` 메소드를 사용할 수 있습니다:

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
<!-- ### Raw Methods -->
### Raw Methods

<!-- Instead of using the `DB::raw` method, you may also use the following methods to insert a raw expression into various parts of your query. **Remember, Laravel cannot guarantee that any query using raw expressions is protected against SQL injection vulnerabilities.** -->
`DB::raw` 방법을 사용하는 대신 다음 방법을 사용하여 쿼리의 다양한 부분에 원시 표현식을 삽입할 수도 있습니다. **Laravel는 원시 표현식을 사용하는 쿼리가 SQL 주입 취약점으로부터 보호된다는 점을 보장할 수 없습니다.**

<a name="selectraw"></a>
<!-- #### `selectRaw` -->
#### `selectRaw`

<!-- The `selectRaw` method can be used in place of `addSelect(DB::raw(/* ... */))`. This method accepts an optional array of bindings as its second argument: -->
`selectRaw` 방법은 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 이 메소드는 두 번째 인수로 선택적 바인딩 배열을 허용합니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
<!-- #### `whereRaw / orWhereRaw` -->
#### `whereRaw / orWhereRaw`

<!-- The `whereRaw` and `orWhereRaw` methods can be used to inject a raw "where" clause into your query. These methods accept an optional array of bindings as their second argument: -->
`whereRaw` 및 `orWhereRaw` 메소드를 사용하여 쿼리에 원시 "where" 절을 삽입할 수 있습니다. 이 메소드는 두 번째 인수로 선택적 바인딩 배열을 허용합니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
<!-- #### `havingRaw / orHavingRaw` -->
#### `havingRaw / orHavingRaw`

<!-- The `havingRaw` and `orHavingRaw` methods may be used to provide a raw string as the value of the "having" clause. These methods accept an optional array of bindings as their second argument: -->
`havingRaw` 및 `orHavingRaw` 메소드는 "having" 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다. 이 메소드는 두 번째 인수로 선택적 바인딩 배열을 허용합니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
<!-- #### `orderByRaw` -->
#### `orderByRaw`

<!-- The `orderByRaw` method may be used to provide a raw string as the value of the "order by" clause: -->
`orderByRaw` 메소드는 "order by" 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
<!-- ### `groupByRaw` -->
### `groupByRaw`

<!-- The `groupByRaw` method may be used to provide a raw string as the value of the `group by` clause: -->
`groupByRaw` 메소드는 `group by` 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
<!-- ## Joins -->
## Joins

<a name="inner-join-clause"></a>
<!-- #### Inner Join Clause -->
#### Inner Join Clause

<!-- The query builder may also be used to add join clauses to your queries. To perform a basic "inner join", you may use the `join` method on a query builder instance. The first argument passed to the `join` method is the name of the table you need to join to, while the remaining arguments specify the column constraints for the join. You may even join multiple tables in a single query: -->
쿼리 빌더를 사용하여 쿼리에 조인 절을 추가할 수도 있습니다. 기본적인 "내부 조인"을 수행하려면 쿼리 빌더 인스턴스에서 `join` 메소드를 사용할 수 있습니다. `join` 메소드에 전달된 첫 번째 인수는 조인해야 하는 테이블의 이름이고 나머지 인수는 조인에 대한 열 제약 조건을 지정합니다. 단일 쿼리에서 여러 테이블을 조인할 수도 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
<!-- #### Left Join / Right Join Clause -->
#### Left Join / Right Join Clause

<!-- If you would like to perform a "left join" or "right join" instead of an "inner join", use the `leftJoin` or `rightJoin` methods. These methods have the same signature as the `join` method: -->
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
<!-- #### Cross Join Clause -->
#### Cross Join Clause

<!-- You may use the `crossJoin` method to perform a "cross join". Cross joins generate a cartesian product between the first table and the joined table: -->
`crossJoin` 방법을 사용하여 "교차 조인"을 수행할 수 있습니다. 교차 조인은 첫 번째 테이블과 조인된 테이블 사이에 데카르트 곱을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
<!-- #### Advanced Join Clauses -->
#### Advanced Join Clauses

<!-- You may also specify more advanced join clauses. To get started, pass a closure as the second argument to the `join` method. The closure will receive a `Illuminate\Database\Query\JoinClause` instance which allows you to specify constraints on the "join" clause: -->
또한 고급 조인 절을 지정할 수도 있습니다. 시작하려면 클로저를 `join` 메서드의 두 번째 인수로 전달하세요. 클로저는 "join" 절에 제약 조건을 지정할 수 있는 `Illuminate\Database\Query\JoinClause` 인스턴스를 수신합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

<!-- If you would like to use a "where" clause on your joins, you may use the `where` and `orWhere` methods provided by the `JoinClause` instance. Instead of comparing two columns, these methods will compare the column against a value: -->
조인에 "where" 절을 사용하려면 `JoinClause` 인스턴스에서 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 두 열을 비교하는 대신 다음 방법은 열을 값과 비교합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
<!-- #### Subquery Joins -->
#### Subquery Joins

<!-- You may use the `joinSub`, `leftJoinSub`, and `rightJoinSub` methods to join a query to a subquery. Each of these methods receives three arguments: the subquery, its table alias, and a closure that defines the related columns. In this example, we will retrieve a collection of users where each user record also contains the `created_at` timestamp of the user's most recently published blog post: -->
`joinSub`, `leftJoinSub` 및 `rightJoinSub` 메서드를 사용하여 쿼리를 하위 쿼리에 조인할 수 있습니다. 각 메소드는 하위 쿼리, 테이블 별칭, 관련 열을 정의하는 클로저라는 세 가지 인수를 받습니다. 이 예에서는 각 사용자 레코드에 사용자가 가장 최근에 게시한 블로그 게시물의 `created_at` 타임스탬프도 포함되어 있는 사용자 컬렉션을 검색합니다.

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
<!-- #### Lateral Joins -->
#### Lateral Joins

> [!WARNING]
> 측면 조인은 현재 PostgreSQL, MySQL >= 8.0.14 및 SQL Server에서 지원됩니다.

<!-- You may use the `joinLateral` and `leftJoinLateral` methods to perform a "lateral join" with a subquery. Each of these methods receives two arguments: the subquery and its table alias. The join condition(s) should be specified within the `where` clause of the given subquery. Lateral joins are evaluated for each row and can reference columns outside the subquery. -->
하위 쿼리로 "측면 조인"을 수행하려면 `joinLateral` 및 `leftJoinLateral` 메서드를 사용할 수 있습니다. 이러한 각 메서드는 하위 쿼리와 해당 테이블 별칭이라는 두 가지 인수를 받습니다. 조인 조건은 해당 하위 쿼리의 `where` 절 내에 지정되어야 합니다. 측면 조인은 각 행에 대해 평가되며 하위 쿼리 외부의 열을 참조할 수 있습니다.

<!-- In this example, we will retrieve a collection of users as well as the user's three most recent blog posts. Each user can produce up to three rows in the result set: one for each of their most recent blog posts. The join condition is specified with a `whereColumn` clause within the subquery, referencing the current user row: -->
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
<!-- ## Unions -->
## Unions

<!-- The query builder also provides a convenient method to "union" two or more queries together. For example, you may create an initial query and use the `union` method to union it with more queries: -->
쿼리 빌더는 둘 이상의 쿼리를 함께 "결합"하는 편리한 방법도 제공합니다. 예를 들어 초기 쿼리를 생성하고 `union` 메서드를 사용하여 이를 더 많은 쿼리와 결합할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$usersWithoutFirstName = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($usersWithoutFirstName)
    ->get();
```

<!-- In addition to the `union` method, the query builder provides a `unionAll` method. Queries that are combined using the `unionAll` method will not have their duplicate results removed. The `unionAll` method has the same method signature as the `union` method. -->
`union` 메소드 외에도 쿼리 빌더는 `unionAll` 메소드를 제공합니다. `unionAll` 방법을 사용하여 결합된 쿼리는 중복 결과가 제거되지 않습니다. `unionAll` 메서드는 `union` 메서드와 동일한 메서드 서명을 갖습니다.

<a name="basic-where-clauses"></a>
<!-- ## Basic Where Clauses -->
## Basic Where Clauses

<a name="where-clauses"></a>
<!-- ### Where Clauses -->
### Where Clauses

<!-- You may use the query builder's `where` method to add "where" clauses to the query. The most basic call to the `where` method requires three arguments. The first argument is the name of the column. The second argument is an operator, which can be any of the database's supported operators. The third argument is the value to compare against the column's value. -->
쿼리 빌더의 `where` 메소드를 사용하여 쿼리에 "where" 절을 추가할 수 있습니다. `where` 메서드에 대한 가장 기본적인 호출에는 세 가지 인수가 필요합니다. 첫 번째 인수는 열의 이름입니다. 두 번째 인수는 데이터베이스가 지원하는 연산자 중 하나일 수 있는 연산자입니다. 세 번째 인수는 열의 값과 비교할 값입니다.

<!-- For example, the following query retrieves users where the value of the `votes` column is equal to `100` and the value of the `age` column is greater than `35`: -->
예를 들어, 다음 쿼리는 `votes` 열의 값이 `100`와 같고 `age` 열의 값이 `35`보다 큰 사용자를 검색합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

<!-- For convenience, if you want to verify that a column is `=` to a given value, you may pass the value as the second argument to the `where` method. Laravel will assume you would like to use the `=` operator: -->
편의상 해당 열이 주어진 값에 대해 `=`인지 확인하려는 경우 해당 값을 `where` 메서드의 두 번째 인수로 전달할 수 있습니다. Laravel는 `=` 연산자를 사용한다고 가정합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

<!-- You may also provide an associative array to the `where` method to quickly query against multiple columns: -->
여러 열에 대해 쿼리를 신속하게 처리하기 위해 `where` 메서드에 연관 배열을 제공할 수도 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

<!-- As previously mentioned, you may use any operator that is supported by your database system: -->
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

<!-- You may also pass an array of conditions to the `where` function. Each element of the array should be an array containing the three arguments typically passed to the `where` method: -->
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
<!-- ### Or Where Clauses -->
### Or Where Clauses

<!-- When chaining together calls to the query builder's `where` method, the "where" clauses will be joined together using the `and` operator. However, you may use the `orWhere` method to join a clause to the query using the `or` operator. The `orWhere` method accepts the same arguments as the `where` method: -->
쿼리 빌더의 `where` 메소드에 대한 호출을 함께 연결할 때 "where" 절은 `and` 연산자를 사용하여 함께 결합됩니다. 그러나 `or` 연산자를 사용하여 절을 쿼리에 조인하려면 `orWhere` 메서드를 사용할 수 있습니다. `orWhere` 메서드는 `where` 메서드와 동일한 인수를 허용합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

<!-- If you need to group an "or" condition within parentheses, you may pass a closure as the first argument to the `orWhere` method: -->
괄호 안에 "or" 조건을 그룹화해야 하는 경우 클로저를 `orWhere` 메소드의 첫 번째 인수로 전달할 수 있습니다.

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

<!-- The example above will produce the following SQL: -->
위의 예에서는 다음 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 범위가 적용될 때 예기치 않은 동작을 방지하려면 항상 `orWhere` 호출을 그룹화해야 합니다.

<a name="where-not-clauses"></a>
<!-- ### Where Not Clauses -->
### Where Not Clauses

<!-- The `whereNot` and `orWhereNot` methods may be used to negate a given group of query constraints. For example, the following query excludes products that are on clearance or which have a price that is less than ten: -->
`whereNot` 및 `orWhereNot` 메소드는 지정된 쿼리 제약 조건 그룹을 무효화하는 데 사용될 수 있습니다. 예를 들어, 다음 쿼리는 재고 정리 중이거나 가격이 10보다 낮은 제품을 제외합니다.

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
<!-- ### Where Any / All / None Clauses -->
### Where Any / All / None Clauses

<!-- Sometimes you may need to apply the same query constraints to multiple columns. For example, you may want to retrieve all records where any columns in a given list are `LIKE` a given value. You may accomplish this using the `whereAny` method: -->
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

<!-- The query above will result in the following SQL: -->
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

<!-- Similarly, the `whereAll` method may be used to retrieve records where all of the given columns match a given constraint: -->
마찬가지로, `whereAll` 메소드는 주어진 모든 열이 주어진 제약 조건과 일치하는 레코드를 검색하는 데 사용될 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

<!-- The query above will result in the following SQL: -->
위의 쿼리는 다음 SQL을 생성합니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

<!-- The `whereNone` method may be used to retrieve records where none of the given columns match a given constraint: -->
`whereNone` 메소드는 주어진 열 중 어느 것도 주어진 제약 조건과 일치하지 않는 레코드를 검색하는 데 사용할 수 있습니다.

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

<!-- The query above will result in the following SQL: -->
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
<!-- ### JSON Where Clauses -->
### JSON Where Clauses

<!-- Laravel also supports querying JSON column types on databases that provide support for JSON column types. Currently, this includes MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, and SQLite 3.39.0+. To query a JSON column, use the `->` operator: -->
Laravel는 JSON 열 유형에 대한 지원을 제공하는 데이터베이스에서 JSON 열 유형 쿼리도 지원합니다. 현재 여기에는 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+ 및 SQLite 3.39.0+가 포함됩니다. JSON 열을 쿼리하려면 `->` 연산자를 사용하세요.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

<!-- You may use the `whereJsonContains` and `whereJsonDoesntContain` methods to query JSON arrays: -->
쿼리 JSON 배열에 `whereJsonContains` 및 `whereJsonDoesntContain` 방법을 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

<!-- If your application uses the MariaDB, MySQL, or PostgreSQL databases, you may pass an array of values to the `whereJsonContains` and `whereJsonDoesntContain` methods: -->
애플리케이션이 MariaDB, MySQL 또는 PostgreSQL 데이터베이스를 사용하는 경우 값 배열을 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드에 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

<!-- In addition, you may use the `whereJsonContainsKey` or `whereJsonDoesntContainKey` methods to retrieve the results that include or do not include a JSON key: -->
또한 `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용하여 JSON 키를 포함하거나 포함하지 않는 결과를 검색할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

<!-- Finally, you may use `whereJsonLength` method to query JSON arrays by their length: -->
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
<!-- ### Additional Where Clauses -->
### Additional Where Clauses

<!-- **whereLike / orWhereLike / whereNotLike / orWhereNotLike** -->
**어디처럼/또는어디처럼/어디같지 않음/또는어디같지 않음**

<!-- The `whereLike` method allows you to add "LIKE" clauses to your query for pattern matching. These methods provide a database-agnostic way of performing string matching queries, with the ability to toggle case-sensitivity. By default, string matching is case-insensitive: -->
`whereLike` 메소드를 사용하면 패턴 일치를 위해 쿼리에 "LIKE" 절을 추가할 수 있습니다. 이러한 방법은 대소문자 구분을 전환하는 기능과 함께 문자열 일치 쿼리를 수행하는 데이터베이스에 구애받지 않는 방법을 제공합니다. 기본적으로 문자열 일치는 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

<!-- You can enable a case-sensitive search via the `caseSensitive` argument: -->
`caseSensitive` 인수를 통해 대소문자 구분 검색을 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

<!-- The `orWhereLike` method allows you to add an "or" clause with a LIKE condition: -->
`orWhereLike` 메소드를 사용하면 LIKE 조건과 함께 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

<!-- The `whereNotLike` method allows you to add "NOT LIKE" clauses to your query: -->
`whereNotLike` 메소드를 사용하면 쿼리에 "NOT LIKE" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

<!-- Similarly, you can use `orWhereNotLike` to add an "or" clause with a NOT LIKE condition: -->
마찬가지로 `orWhereNotLike`를 사용하여 NOT LIKE 조건과 함께 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike` 대/소문자 구분 검색 옵션은 현재 SQL Server에서 지원되지 않습니다.

<!-- **whereIn / whereNotIn / orWhereIn / orWhereNotIn** -->
**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

<!-- The `whereIn` method verifies that a given column's value is contained within the given array: -->
`whereIn` 메소드는 주어진 열의 값이 주어진 배열 내에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

<!-- The `whereNotIn` method verifies that the given column's value is not contained in the given array: -->
`whereNotIn` 메소드는 주어진 열의 값이 주어진 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

<!-- You may also provide a query object as the `whereIn` method's second argument: -->
`whereIn` 메소드의 두 번째 인수로 쿼리 객체를 제공할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

<!-- The example above will produce the following SQL: -->
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

<!-- **whereBetween / orWhereBetween** -->
**어디 사이에 / 또는어디 사이에**

<!-- The `whereBetween` method verifies that a column's value is between two values: -->
`whereBetween` 메서드는 열 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

<!-- **whereNotBetween / orWhereNotBetween** -->
**Between / 또는WhereNotBetween**

<!-- The `whereNotBetween` method verifies that a column's value lies outside of two values: -->
`whereNotBetween` 메서드는 열 값이 두 값 외부에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

<!-- **whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns** -->
**whereBetweenColumns / whereNotBetweenColumns / 또는WhereBetweenColumns / 또는WhereNotBetweenColumns**

<!-- The `whereBetweenColumns` method verifies that a column's value is between the two values of two columns in the same table row: -->
`whereBetweenColumns` 메서드는 열 값이 동일한 테이블 행에 있는 두 열의 두 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

<!-- The `whereNotBetweenColumns` method verifies that a column's value lies outside the two values of two columns in the same table row: -->
`whereNotBetweenColumns` 메서드는 열 값이 동일한 테이블 행에 있는 두 열의 두 값 외부에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

<!-- **whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween** -->
**사이에 있는 값 / 사이에 없는 값 / 또는 사이에 있는 값 / 또는 사이에 없는 값**

<!-- The `whereValueBetween` method verifies that a given value is between the values of two columns of the same type in the same table row: -->
`whereValueBetween` 메서드는 지정된 값이 동일한 테이블 행에 있는 동일한 유형의 두 열 값 사이에 있는지 확인합니다.

```php
$products = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

<!-- The `whereValueNotBetween` method verifies that a value lies outside the values of two columns in the same table row: -->
`whereValueNotBetween` 메서드는 값이 동일한 테이블 행에 있는 두 열의 값 외부에 있는지 확인합니다.

```php
$products = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

<!-- **whereNull / whereNotNull / orWhereNull / orWhereNotNull** -->
**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

<!-- The `whereNull` method verifies that the value of the given column is `NULL`: -->
`whereNull` 메소드는 주어진 열의 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

<!-- The `whereNotNull` method verifies that the column's value is not `NULL`: -->
`whereNotNull` 메소드는 열의 값이 `NULL`가 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

<!-- **whereDate / whereMonth / whereDay / whereYear / whereTime** -->
**whereDate / whereMonth / whereDay / whereYear / whereTime**

<!-- The `whereDate` method may be used to compare a column's value against a date: -->
`whereDate` 메소드는 열의 값을 날짜와 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

<!-- The `whereMonth` method may be used to compare a column's value against a specific month: -->
`whereMonth` 메소드는 열의 값을 특정 월과 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

<!-- The `whereDay` method may be used to compare a column's value against a specific day of the month: -->
`whereDay` 메소드는 열의 값을 특정 날짜와 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

<!-- The `whereYear` method may be used to compare a column's value against a specific year: -->
`whereYear` 메소드는 열의 값을 특정 연도와 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

<!-- The `whereTime` method may be used to compare a column's value against a specific time: -->
`whereTime` 메소드는 열의 값을 특정 시간과 비교하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

<!-- **wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday** -->
**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

<!-- The `wherePast` and `whereFuture` methods may be used to determine if a column's value is in the past or future: -->
`wherePast` 및 `whereFuture` 메소드는 열의 값이 과거인지 미래인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

<!-- The `whereNowOrPast` and `whereNowOrFuture` methods may be used to determine if a column's value is in the past or future, inclusive of the current date and time: -->
`whereNowOrPast` 및 `whereNowOrFuture` 메소드는 열의 값이 현재 날짜와 시간을 포함하여 과거인지 미래인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

<!-- The `whereToday`, `whereBeforeToday`, and `whereAfterToday` methods may be used to determine if a column's value is today, before today, or after today, respectively: -->
`whereToday`, `whereBeforeToday` 및 `whereAfterToday` 메소드는 열의 값이 각각 오늘, 오늘 이전 또는 오늘 이후인지 확인하는 데 사용할 수 있습니다.

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

<!-- Similarly, the `whereTodayOrBefore` and `whereTodayOrAfter` methods may be used to determine if a column's value is before today or after today, inclusive of today's date: -->
마찬가지로 `whereTodayOrBefore` 및 `whereTodayOrAfter` 메서드를 사용하여 열의 값이 오늘 날짜를 포함하여 오늘 이전인지 오늘 이후인지 확인할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

<!-- **whereColumn / orWhereColumn** -->
**whereColumn / 또는WhereColumn**

<!-- The `whereColumn` method may be used to verify that two columns are equal: -->
`whereColumn` 메서드를 사용하여 두 열이 동일한지 확인할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

<!-- You may also pass a comparison operator to the `whereColumn` method: -->
`whereColumn` 메소드에 비교 연산자를 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

<!-- You may also pass an array of column comparisons to the `whereColumn` method. These conditions will be joined using the `and` operator: -->
열 비교 배열을 `whereColumn` 메소드에 전달할 수도 있습니다. 이러한 조건은 `and` 연산자를 사용하여 결합됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
<!-- ### Logical Grouping -->
### Logical Grouping

<!-- Sometimes you may need to group several "where" clauses within parentheses in order to achieve your query's desired logical grouping. In fact, you should generally always group calls to the `orWhere` method in parentheses in order to avoid unexpected query behavior. To accomplish this, you may pass a closure to the `where` method: -->
때로는 쿼리의 원하는 논리적 그룹화를 달성하기 위해 괄호 안에 여러 "where" 절을 그룹화해야 할 수도 있습니다. 실제로 예기치 않은 쿼리 동작을 방지하려면 일반적으로 항상 `orWhere` 메서드에 대한 호출을 괄호로 그룹화해야 합니다. 이를 달성하려면 `where` 메소드에 클로저를 전달할 수 있습니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

<!-- As you can see, passing a closure into the `where` method instructs the query builder to begin a constraint group. The closure will receive a query builder instance which you can use to set the constraints that should be contained within the parenthesis group. The example above will produce the following SQL: -->
보시다시피 클로저를 `where` 메소드에 전달하면 쿼리 빌더에 제약 조건 그룹을 시작하도록 지시합니다. 클로저는 괄호 그룹 내에 포함되어야 하는 제약 조건을 설정하는 데 사용할 수 있는 쿼리 빌더 인스턴스를 수신합니다. 위의 예에서는 다음 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 범위가 적용될 때 예기치 않은 동작을 방지하려면 항상 `orWhere` 호출을 그룹화해야 합니다.

<a name="advanced-where-clauses"></a>
<!-- ## Advanced Where Clauses -->
## Advanced Where Clauses

<a name="where-exists-clauses"></a>
<!-- ### Where Exists Clauses -->
### Where Exists Clauses

<!-- The `whereExists` method allows you to write "where exists" SQL clauses. The `whereExists` method accepts a closure which will receive a query builder instance, allowing you to define the query that should be placed inside of the "exists" clause: -->
`whereExists` 메소드를 사용하면 "존재하는 위치" SQL 절을 작성할 수 있습니다. `whereExists` 메소드는 쿼리 빌더 인스턴스를 수신하는 클로저를 허용하므로 "exists" 절 내부에 배치되어야 하는 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

<!-- Alternatively, you may provide a query object to the `whereExists` method instead of a closure: -->
또는 클로저 대신 쿼리 객체를 `whereExists` 메소드에 제공할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

<!-- Both of the examples above will produce the following SQL: -->
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
<!-- ### Subquery Where Clauses -->
### Subquery Where Clauses

<!-- Sometimes you may need to construct a "where" clause that compares the results of a subquery to a given value. You may accomplish this by passing a closure and a value to the `where` method. For example, the following query will retrieve all users who have a recent "membership" of a given type; -->
때로는 하위 쿼리의 결과를 주어진 값과 비교하는 "where" 절을 구성해야 할 수도 있습니다. `where` 메소드에 클로저와 값을 전달하여 이를 수행할 수 있습니다. 예를 들어, 다음 쿼리는 특정 유형의 최근 "멤버십"을 가진 모든 사용자를 검색합니다.

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

<!-- Or, you may need to construct a "where" clause that compares a column to the results of a subquery. You may accomplish this by passing a column, operator, and closure to the `where` method. For example, the following query will retrieve all income records where the amount is less than average; -->
또는 하위 쿼리 결과와 열을 비교하는 "where" 절을 구성해야 할 수도 있습니다. 열, 연산자 및 클로저를 `where` 메소드에 전달하여 이를 수행할 수 있습니다. 예를 들어, 다음 쿼리는 금액이 평균보다 적은 모든 소득 기록을 검색합니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
<!-- ### Full Text Where Clauses -->
### Full Text Where Clauses

> [!WARNING]
> 절이 현재 MariaDB, MySQL 및 PostgreSQL에서 지원되는 전체 텍스트입니다.

<!-- The `whereFullText` and `orWhereFullText` methods may be used to add full text "where" clauses to a query for columns that have [full text indexes](/docs/12.x/migrations#available-index-types). These methods will be transformed into the appropriate SQL for the underlying database system by Laravel. For example, a `MATCH AGAINST` clause will be generated for applications utilizing MariaDB or MySQL: -->
`whereFullText` 및 `orWhereFullText` 메서드는 [full text indexes](/docs/12.x/migrations#available-index-types)가 있는 열의 쿼리에 전체 텍스트 "where" 절을 추가하는 데 사용할 수 있습니다. 이러한 메소드는 Laravel에 의해 기본 데이터베이스 시스템에 적합한 SQL로 변환됩니다. 예를 들어, MariaDB 또는 MySQL을 활용하는 애플리케이션에 대해 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
<!-- ### Vector Similarity Clauses -->
### Vector Similarity Clauses

> [!NOTE]
> 벡터 유사성 절은 현재 `pgvector` 확장을 사용하는 PostgreSQL 연결에서만 지원됩니다. 벡터 열 및 인덱스 정의에 대한 자세한 내용은 [migration documentation](/docs/12.x/migrations#available-column-types)를 참조하세요.

<!-- The `whereVectorSimilarTo` method filters results by cosine similarity to a given vector and orders the results by relevance. The `minSimilarity` threshold should be a value between `0.0` and `1.0`, where `1.0` is identical: -->
`whereVectorSimilarTo` 방법은 주어진 벡터에 대한 코사인 유사성을 기준으로 결과를 필터링하고 관련성에 따라 결과를 정렬합니다. `minSimilarity` 임계값은 `0.0`와 `1.0` 사이의 값이어야 합니다. 여기서 `1.0`는 동일합니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

<!-- When a plain string is given as the vector argument, Laravel will automatically generate embeddings for it using the [Laravel AI SDK](/docs/12.x/ai-sdk#embeddings): -->
일반 문자열이 벡터 인수로 제공되면 Laravel는 [Laravel AI SDK](/docs/12.x/ai-sdk#embeddings)를 사용하여 자동으로 임베딩을 생성합니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

<!-- By default, `whereVectorSimilarTo` also orders results by distance (most similar first). You may disable this ordering by passing `false` as the `order` argument: -->
기본적으로 `whereVectorSimilarTo`는 거리별로 결과를 정렬합니다(가장 유사한 것부터). `false`를 `order` 인수로 전달하여 이 순서를 비활성화할 수 있습니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

<!-- If you need more control, you may use the `selectVectorDistance`, `whereVectorDistanceLessThan`, and `orderByVectorDistance` methods independently: -->
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

<!-- When utilizing PostgreSQL, the `pgvector` extension must be loaded before `vector` columns can be created: -->
PostgreSQL를 활용하는 경우 `vector` 열을 생성하기 전에 `pgvector` 확장을 로드해야 합니다.

```php
Schema::ensureVectorExtensionExists();
```

<a name="ordering-grouping-limit-and-offset"></a>
<!-- ## Ordering, Grouping, Limit and Offset -->
## Ordering, Grouping, Limit and Offset

<a name="ordering"></a>
<!-- ### Ordering -->
### Ordering

<a name="orderby"></a>
<!-- #### The `orderBy` Method -->
#### The `orderBy` Method

<!-- The `orderBy` method allows you to sort the results of the query by a given column. The first argument accepted by the `orderBy` method should be the column you wish to sort by, while the second argument determines the direction of the sort and may be either `asc` or `desc`: -->
`orderBy` 방법을 사용하면 주어진 열을 기준으로 쿼리의 결과를 정렬할 수 있습니다. `orderBy` 메소드에서 허용하는 첫 번째 인수는 정렬하려는 열이어야 하며, 두 번째 인수는 정렬 방향을 결정하며 `asc` 또는 `desc`일 수 있습니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

<!-- To sort by multiple columns, you may simply invoke `orderBy` as many times as necessary: -->
여러 열을 기준으로 정렬하려면 필요한 만큼 `orderBy`를 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

<!-- The sort direction is optional, and is ascending by default. If you want to sort in descending order, you can specify the second parameter for the `orderBy` method, or just use `orderByDesc`: -->
정렬 방향은 선택 사항이며 기본적으로 오름차순입니다. 내림차순으로 정렬하려면 `orderBy` 메서드에 대한 두 번째 매개변수를 지정하거나 `orderByDesc`를 사용하면 됩니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

<!-- Finally, using the `->` operator, the results can be sorted by a value within a JSON column: -->
마지막으로 `->` 연산자를 사용하여 결과를 JSON 열 내의 값을 기준으로 정렬할 수 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
<!-- #### The `latest` and `oldest` Methods -->
#### The `latest` and `oldest` Methods

<!-- The `latest` and `oldest` methods allow you to easily order results by date. By default, the result will be ordered by the table's `created_at` column. Or, you may pass the column name that you wish to sort by: -->
`latest` 및 `oldest` 방법을 사용하면 결과를 날짜별로 쉽게 정렬할 수 있습니다. 기본적으로 결과는 테이블의 `created_at` 열을 기준으로 정렬됩니다. 또는 정렬하려는 열 이름을 전달할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
<!-- #### Random Ordering -->
#### Random Ordering

<!-- The `inRandomOrder` method may be used to sort the query results randomly. For example, you may use this method to fetch a random user: -->
`inRandomOrder` 방법은 쿼리 결과를 무작위로 정렬하는 데 사용될 수 있습니다. 예를 들어, 이 메소드를 사용하여 임의의 사용자를 가져올 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
<!-- #### Removing Existing Orderings -->
#### Removing Existing Orderings

<!-- The `reorder` method removes all of the "order by" clauses that have previously been applied to the query: -->
`reorder` 메소드는 이전에 쿼리에 적용된 "order by" 절을 모두 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

<!-- You may pass a column and direction when calling the `reorder` method in order to remove all existing "order by" clauses and apply an entirely new order to the query: -->
기존의 모든 "order by" 절을 제거하고 완전히 새로운 순서를 쿼리에 적용하기 위해 `reorder` 메서드를 호출할 때 열과 방향을 전달할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<!-- For convenience, you may use the `reorderDesc` method to reorder the query results in descending order: -->
편의를 위해 `reorderDesc` 메소드를 사용하여 쿼리 결과를 내림차순으로 재정렬할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
<!-- ### Grouping -->
### Grouping

<a name="groupby-having"></a>
<!-- #### The `groupBy` and `having` Methods -->
#### The `groupBy` and `having` Methods

<!-- As you might expect, the `groupBy` and `having` methods may be used to group the query results. The `having` method's signature is similar to that of the `where` method: -->
예상할 수 있듯이 `groupBy` 및 `having` 메서드를 사용하여 쿼리 결과를 그룹화할 수 있습니다. `having` 메소드의 서명은 `where` 메소드의 서명과 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

<!-- You can use the `havingBetween` method to filter the results within a given range: -->
`havingBetween` 메서드를 사용하여 지정된 범위 내에서 결과를 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

<!-- You may pass multiple arguments to the `groupBy` method to group by multiple columns: -->
여러 열로 그룹화하기 위해 `groupBy` 메서드에 여러 인수를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

<!-- To build more advanced `having` statements, see the [havingRaw](#raw-methods) method. -->
고급 `having` 문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참조하세요.

<a name="limit-and-offset"></a>
<!-- ### Limit and Offset -->
### Limit and Offset

<!-- You may use the `limit` and `offset` methods to limit the number of results returned from the query or to skip a given number of results in the query: -->
`limit` 및 `offset` 메소드를 사용하여 쿼리에서 반환되는 결과 수를 제한하거나 쿼리에서 지정된 수의 결과를 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
<!-- ## Conditional Clauses -->
## Conditional Clauses

<!-- Sometimes you may want certain query clauses to apply to a query based on another condition. For instance, you may only want to apply a `where` statement if a given input value is present on the incoming HTTP request. You may accomplish this using the `when` method: -->
때로는 특정 쿼리 절을 다른 조건에 따라 쿼리에 적용하기를 원할 수도 있습니다. 예를 들어, 들어오는 HTTP 요청에 지정된 입력 값이 있는 경우에만 `where` 문을 적용할 수 있습니다. `when` 방법을 사용하여 이 작업을 수행할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

<!-- The `when` method only executes the given closure when the first argument is `true`. If the first argument is `false`, the closure will not be executed. So, in the example above, the closure given to the `when` method will only be invoked if the `role` field is present on the incoming request and evaluates to `true`. -->
`when` 메소드는 첫 번째 인수가 `true`인 경우에만 지정된 클로저를 실행합니다. 첫 번째 인수가 `false`이면 클로저가 실행되지 않습니다. 따라서 위의 예에서 `when` 메서드에 제공된 클로저는 들어오는 요청에 `role` 필드가 있고 `true`로 평가되는 경우에만 호출됩니다.

<!-- You may pass another closure as the third argument to the `when` method. This closure will only execute if the first argument evaluates as `false`. To illustrate how this feature may be used, we will use it to configure the default ordering of a query: -->
`when` 메소드의 세 번째 인수로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 첫 번째 인수가 `false`로 평가되는 경우에만 실행됩니다. 이 기능을 사용하는 방법을 설명하기 위해 이 기능을 사용하여 쿼리의 기본 순서를 구성하겠습니다.

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
<!-- ## Insert Statements -->
## Insert Statements

<!-- The query builder also provides an `insert` method that may be used to insert records into the database table. The `insert` method accepts an array of column names and values: -->
쿼리 빌더는 데이터베이스 테이블에 레코드를 삽입하는 데 사용할 수 있는 `insert` 메소드도 제공합니다. `insert` 메서드는 열 이름과 값의 배열을 허용합니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

<!-- You may insert several records at once by passing an array of arrays. Each array represents a record that should be inserted into the table: -->
배열의 배열을 전달하여 여러 레코드를 한 번에 삽입할 수 있습니다. 각 배열은 테이블에 삽입되어야 하는 레코드를 나타냅니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

<!-- The `insertOrIgnore` method will ignore errors while inserting records into the database. When using this method, you should be aware that duplicate record errors will be ignored and other types of errors may also be ignored depending on the database engine. For example, `insertOrIgnore` will [bypass MySQL's strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution): -->
`insertOrIgnore` 메소드는 데이터베이스에 레코드를 삽입하는 동안 오류를 무시합니다. 이 방법을 사용할 경우 중복 레코드 오류는 무시되며, 데이터베이스 엔진에 따라 다른 유형의 오류도 무시될 수 있다는 점을 유의해야 합니다. 예를 들어, `insertOrIgnore`는 [bypass MySQL's strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

<!-- The `insertUsing` method will insert new records into the table while using a subquery to determine the data that should be inserted: -->
`insertUsing` 메소드는 삽입되어야 하는 데이터를 결정하기 위해 하위 쿼리를 사용하는 동안 테이블에 새 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
<!-- #### Auto-Incrementing IDs -->
#### Auto-Incrementing IDs

<!-- If the table has an auto-incrementing id, use the `insertGetId` method to insert a record and then retrieve the ID: -->
테이블에 자동 증가 ID가 있는 경우 `insertGetId` 메서드를 사용하여 레코드를 삽입한 다음 ID를 검색합니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL를 사용할 때 `insertGetId` 메서드는 자동 증가 열의 이름이 `id`일 것으로 예상합니다. 다른 "시퀀스"에서 ID를 검색하려면 열 이름을 `insertGetId` 메소드의 두 번째 매개변수로 전달할 수 있습니다.

<a name="upserts"></a>
<!-- ### Upserts -->
### Upserts

<!-- The `upsert` method will insert records that do not exist and update the records that already exist with new values that you may specify. The method's first argument consists of the values to insert or update, while the second argument lists the column(s) that uniquely identify records within the associated table. The method's third and final argument is an array of columns that should be updated if a matching record already exists in the database: -->
`upsert` 메소드는 존재하지 않는 레코드를 삽입하고 이미 존재하는 레코드를 사용자가 지정할 수 있는 새 값으로 업데이트합니다. 메서드의 첫 번째 인수는 삽입하거나 업데이트할 값으로 구성되며, 두 번째 인수는 연결된 테이블 내에서 레코드를 고유하게 식별하는 열을 나열합니다. 메소드의 세 번째이자 마지막 인수는 데이터베이스에 일치하는 레코드가 이미 있는 경우 업데이트해야 하는 열 배열입니다.

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

<!-- In the example above, Laravel will attempt to insert two records. If a record already exists with the same `departure` and `destination` column values, Laravel will update that record's `price` column. -->
위의 예에서 Laravel는 두 개의 레코드를 삽입하려고 시도합니다. 동일한 `departure` 및 `destination` 열 값을 가진 레코드가 이미 존재하는 경우 Laravel는 해당 레코드의 `price` 열을 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수 열에 "기본" 또는 "고유" 인덱스가 있어야 합니다. 또한 MariaDB 및 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하고 항상 테이블의 "기본" 및 "고유" 인덱스를 사용하여 기존 레코드를 검색합니다.

<a name="update-statements"></a>
<!-- ## Update Statements -->
## Update Statements

<!-- In addition to inserting records into the database, the query builder can also update existing records using the `update` method. The `update` method, like the `insert` method, accepts an array of column and value pairs indicating the columns to be updated. The `update` method returns the number of affected rows. You may constrain the `update` query using `where` clauses: -->
데이터베이스에 레코드를 삽입하는 것 외에도 쿼리 빌더는 `update` 메소드를 사용하여 기존 레코드를 업데이트할 수도 있습니다. `update` 메서드는 `insert` 메서드와 마찬가지로 업데이트할 열을 나타내는 열 및 값 쌍의 배열을 허용합니다. `update` 메서드는 영향을 받은 행 수를 반환합니다. `where` 절을 사용하여 `update` 쿼리를 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
<!-- #### Update or Insert -->
#### Update or Insert

<!-- Sometimes you may want to update an existing record in the database or create it if no matching record exists. In this scenario, the `updateOrInsert` method may be used. The `updateOrInsert` method accepts two arguments: an array of conditions by which to find the record, and an array of column and value pairs indicating the columns to be updated. -->
때로는 데이터베이스의 기존 레코드를 업데이트하거나 일치하는 레코드가 없는 경우 이를 생성해야 할 수도 있습니다. 이 시나리오에서는 `updateOrInsert` 메서드를 사용할 수 있습니다. `updateOrInsert` 메소드는 두 개의 인수, 즉 레코드를 찾는 조건의 배열과 업데이트할 열을 나타내는 열 및 값 쌍의 배열을 허용합니다.

<!-- The `updateOrInsert` method will attempt to locate a matching database record using the first argument's column and value pairs. If the record exists, it will be updated with the values in the second argument. If the record cannot be found, a new record will be inserted with the merged attributes of both arguments: -->
`updateOrInsert` 메소드는 첫 번째 인수의 열과 값 쌍을 사용하여 일치하는 데이터베이스 레코드를 찾으려고 시도합니다. 레코드가 존재하는 경우 두 번째 인수의 값으로 업데이트됩니다. 레코드를 찾을 수 없는 경우 두 인수의 병합된 속성을 사용하여 새 레코드가 삽입됩니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<!-- You may provide a closure to the `updateOrInsert` method to customize the attributes that are updated or inserted into the database based on the existence of a matching record: -->
일치하는 레코드의 존재에 따라 데이터베이스에 업데이트되거나 삽입되는 속성을 사용자 지정하기 위해 `updateOrInsert` 메소드에 대한 클로저를 제공할 수 있습니다.

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
<!-- ### Updating JSON Columns -->
### Updating JSON Columns

<!-- When updating a JSON column, you should use `->` syntax to update the appropriate key in the JSON object. This operation is supported on MariaDB 10.3+, MySQL 5.7+, and PostgreSQL 9.5+: -->
JSON 열을 업데이트할 때 `->` 구문을 사용하여 JSON 개체에서 적절한 키를 업데이트해야 합니다. 이 작업은 MariaDB 10.3+, MySQL 5.7+ 및 PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
<!-- ### Increment and Decrement -->
### Increment and Decrement

<!-- The query builder also provides convenient methods for incrementing or decrementing the value of a given column. Both of these methods accept at least one argument: the column to modify. A second argument may be provided to specify the amount by which the column should be incremented or decremented: -->
쿼리 빌더는 지정된 열의 값을 늘리거나 줄이는 편리한 방법도 제공합니다. 이 두 가지 방법 모두 최소한 하나의 인수(수정할 열)를 허용합니다. 열이 증가하거나 감소해야 하는 양을 지정하기 위해 두 번째 인수가 제공될 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

<!-- If needed, you may also specify additional columns to update during the increment or decrement operation: -->
필요한 경우 증가 또는 감소 작업 중에 업데이트할 추가 열을 지정할 수도 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

<!-- In addition, you may increment or decrement multiple columns at once using the `incrementEach` and `decrementEach` methods: -->
또한 `incrementEach` 및 `decrementEach` 메서드를 사용하여 한 번에 여러 열을 늘리거나 줄일 수 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
<!-- ## Delete Statements -->
## Delete Statements

<!-- The query builder's `delete` method may be used to delete records from the table. The `delete` method returns the number of affected rows. You may constrain `delete` statements by adding "where" clauses before calling the `delete` method: -->
쿼리 빌더의 `delete` 메소드를 사용하여 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 행 수를 반환합니다. `delete` 메소드를 호출하기 전에 "where" 절을 추가하여 `delete` 문을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
<!-- ## Pessimistic Locking -->
## Pessimistic Locking

<!-- The query builder also includes a few functions to help you achieve "pessimistic locking" when executing your `select` statements. To execute a statement with a "shared lock", you may call the `sharedLock` method. A shared lock prevents the selected rows from being modified until your transaction is committed: -->
쿼리 빌더에는 `select` 문을 실행할 때 "비관적 잠금"을 달성하는 데 도움이 되는 몇 가지 기능도 포함되어 있습니다. "공유 잠금"이 포함된 명령문을 실행하려면 `sharedLock` 메소드를 호출하면 됩니다. 공유 잠금은 트랜잭션이 커밋될 때까지 선택한 행이 수정되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

<!-- Alternatively, you may use the `lockForUpdate` method. A "for update" lock prevents the selected records from being modified or from being selected with another shared lock: -->
또는 `lockForUpdate` 방법을 사용할 수도 있습니다. "업데이트용" 잠금은 선택한 레코드가 수정되거나 다른 공유 잠금으로 선택되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

<!-- While not obligatory, it is recommended to wrap pessimistic locks within a [transaction](/docs/12.x/database#database-transactions). This ensures that the data retrieved remains unaltered in the database until the entire operation completes. In case of a failure, the transaction will roll back any changes and release the locks automatically: -->
필수는 아니지만 [transaction](/docs/12.x/database#database-transactions) 내에서 비관적 잠금을 래핑하는 것이 좋습니다. 이렇게 하면 검색된 데이터가 전체 작업이 완료될 때까지 데이터베이스에서 변경되지 않은 상태로 유지됩니다. 실패할 경우 트랜잭션은 모든 변경 사항을 롤백하고 자동으로 잠금을 해제합니다.

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
<!-- ## Reusable Query Components -->
## Reusable Query Components

<!-- If you have repeated query logic throughout your application, you may extract the logic into reusable objects using the query builder's `tap` and `pipe` methods. Imagine you have these two different queries in your application: -->
애플리케이션 전체에서 쿼리 로직을 반복한 경우 쿼리 빌더의 `tap` 및 `pipe` 메소드를 사용하여 로직을 재사용 가능한 객체로 추출할 수 있습니다. 애플리케이션에 다음 두 가지 쿼리가 있다고 상상해 보세요.

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

<!-- You may like to extract the destination filtering that is common between the queries into a reusable object: -->
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

<!-- Then, you can use the query builder's `tap` method to apply the object's logic to the query: -->
그런 다음 쿼리 빌더의 `tap` 메소드를 사용하여 객체의 논리를 쿼리에 적용할 수 있습니다.

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
<!-- #### Query Pipes -->
#### Query Pipes

<!-- The `tap` method will always return the query builder. If you would like to extract an object that executes the query and returns another value, you may use the `pipe` method instead. -->
`tap` 메소드는 항상 쿼리 빌더를 반환합니다. 쿼리를 실행하고 다른 값을 반환하는 객체를 추출하려면 대신 `pipe` 메서드를 사용할 수 있습니다.

<!-- Consider the following query object that contains shared [pagination](/docs/12.x/pagination) logic used throughout an application. Unlike the `DestinationFilter`, which applies query conditions to the query, the `Paginate` object executes the query and returns a paginator instance: -->
애플리케이션 전체에서 사용되는 공유 [pagination](/docs/12.x/pagination) 논리를 포함하는 다음 쿼리 개체를 고려하세요. 쿼리 조건을 쿼리에 적용하는 `DestinationFilter`와 달리, `Paginate` 객체는 쿼리를 실행하고 페이지네이터 인스턴스를 반환합니다.

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

<!-- Using the query builder's `pipe` method, we can leverage this object to apply our shared pagination logic: -->
쿼리 빌더의 `pipe` 메소드를 사용하면 이 객체를 활용하여 공유 페이지 매김 논리를 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
<!-- ## Debugging -->
## Debugging

<!-- You may use the `dd` and `dump` methods while building a query to dump the current query bindings and SQL. The `dd` method will display the debug information and then stop executing the request. The `dump` method will display the debug information but allow the request to continue executing: -->
현재 쿼리 바인딩 및 SQL을 덤프하기 위해 쿼리를 빌드하는 동안 `dd` 및 `dump` 메서드를 사용할 수 있습니다. `dd` 메서드는 디버그 정보를 표시한 다음 요청 실행을 중지합니다. `dump` 메소드는 디버그 정보를 표시하지만 요청이 계속 실행되도록 허용합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

<!-- The `dumpRawSql` and `ddRawSql` methods may be invoked on a query to dump the query's SQL with all parameter bindings properly substituted: -->
`dumpRawSql` 및 `ddRawSql` 메소드는 쿼리에서 호출되어 모든 매개변수 바인딩이 적절하게 대체된 쿼리의 SQL을 덤프할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
