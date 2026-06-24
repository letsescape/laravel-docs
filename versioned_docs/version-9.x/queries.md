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
    - [JSON Where Clauses](#json-where-clauses)
    - [Additional Where Clauses](#additional-where-clauses)
    - [Logical Grouping](#logical-grouping)
- [Advanced Where Clauses](#advanced-where-clauses)
    - [Where Exists Clauses](#where-exists-clauses)
    - [Subquery Where Clauses](#subquery-where-clauses)
    - [Full Text Where Clauses](#full-text-where-clauses)
- [Ordering, Grouping, Limit & Offset](#ordering-grouping-limit-and-offset)
    - [Ordering](#ordering)
    - [Grouping](#grouping)
    - [Limit & Offset](#limit-and-offset)
- [Conditional Clauses](#conditional-clauses)
- [Insert Statements](#insert-statements)
    - [Upserts](#upserts)
- [Update Statements](#update-statements)
    - [Updating JSON Columns](#updating-json-columns)
    - [Increment & Decrement](#increment-and-decrement)
- [Delete Statements](#delete-statements)
- [Pessimistic Locking](#pessimistic-locking)
- [Debugging](#debugging)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's database query builder provides a convenient, fluent interface to creating and running database queries. It can be used to perform most database operations in your application and works perfectly with all of Laravel's supported database systems. -->
Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽고 유연하게 생성 및 실행할 수 있는 편리한 인터페이스를 제공합니다. 이 빌더는 애플리케이션에서 대부분의 데이터베이스 작업을 수행하는 데 사용할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

<!-- The Laravel query builder uses PDO parameter binding to protect your application against SQL injection attacks. There is no need to clean or sanitize strings passed to the query builder as query bindings. -->
Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 별도로 쿼리 빌더에 전달하는 문자열 값을 정리(clean)하거나 필터링(sanitize)할 필요는 없습니다.

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서, 쿼리에서 참조하는 컬럼 이름(특히 "order by" 컬럼명 등)에 사용자의 입력값이 사용되도록 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
<!-- ## Running Database Queries -->
## Running Database Queries

<a name="retrieving-all-rows-from-a-table"></a>
<!-- #### Retrieving All Rows From A Table -->
#### Retrieving All Rows From A Table

<!-- You may use the `table` method provided by the `DB` facade to begin a query. The `table` method returns a fluent query builder instance for the given table, allowing you to chain more constraints onto the query and then finally retrieve the results of the query using the `get` method: -->
쿼리를 시작하기 위해 `DB` 파사드가 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 쿼리 빌더 인스턴스를 반환하므로, 다양한 제약 조건을 체이닝하여 쿼리를 작성하고 마지막에 `get` 메서드를 통해 결과를 조회할 수 있습니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

<!-- The `get` method returns an `Illuminate\Support\Collection` instance containing the results of the query where each result is an instance of the PHP `stdClass` object. You may access each column's value by accessing the column as a property of the object: -->
`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 여기서 각 결과는 PHP의 `stdClass` 객체로 표현됩니다. 각 컬럼의 값은 객체의 속성(property)으로 접근할 수 있습니다.

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel의 컬렉션은 데이터를 매핑하고 축소(reduce)하는 데 매우 강력한 다양한 메서드를 제공합니다. 컬렉션에 대한 자세한 내용은 [collection documentation](/docs/9.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
<!-- #### Retrieving A Single Row / Column From A Table -->
#### Retrieving A Single Row / Column From A Table

<!-- If you just need to retrieve a single row from a database table, you may use the `DB` facade's `first` method. This method will return a single `stdClass` object: -->
데이터베이스 테이블에서 단일 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

<!-- If you don't need an entire row, you may extract a single value from a record using the `value` method. This method will return the value of the column directly: -->
전체 행이 필요하지 않고 레코드에서 단일 값을 추출하고 싶다면, `value` 메서드를 사용할 수 있습니다. 이 메서드는 해당 컬럼의 값을 바로 반환합니다.

```
$email = DB::table('users')->where('name', 'John')->value('email');
```

<!-- To retrieve a single row by its `id` column value, use the `find` method: -->
`id` 컬럼 값을 기준으로 한 행을 조회하려면, `find` 메서드를 사용할 수 있습니다.

```
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
<!-- #### Retrieving A List Of Column Values -->
#### Retrieving A List Of Column Values

<!-- If you would like to retrieve an `Illuminate\Support\Collection` instance containing the values of a single column, you may use the `pluck` method. In this example, we'll retrieve a collection of user titles: -->
단일 컬럼의 값만을 `Illuminate\Support\Collection` 인스턴스로 조회하고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 다음 예에서는 사용자들의 직함(title)만을 컬렉션으로 가져옵니다.

```
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

<!--  You may specify the column that the resulting collection should use as its keys by providing a second argument to the `pluck` method: -->
`pluck` 메서드의 두 번째 인자로 결과 컬렉션의 키로 사용할 컬럼명을 지정할 수도 있습니다.

```
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
<!-- ### Chunking Results -->
### Chunking Results

<!-- If you need to work with thousands of database records, consider using the `chunk` method provided by the `DB` facade. This method retrieves a small chunk of results at a time and feeds each chunk into a closure for processing. For example, let's retrieve the entire `users` table in chunks of 100 records at a time: -->
수천 개 이상의 데이터베이스 레코드를 한 번에 처리해야 한다면, `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 한 번에 일정량의 결과를 가져와서, 각 청크를 클로저(익명 함수)에 전달하면서 처리할 수 있도록 해줍니다. 아래 예시는 `users` 테이블을 100개씩 조각내어 순차적으로 처리합니다.

```
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    foreach ($users as $user) {
        //
    }
});
```

<!-- You may stop further chunks from being processed by returning `false` from the closure: -->
클로저에서 `false`를 반환하면, 이후 청크 처리는 중단됩니다.

```
DB::table('users')->orderBy('id')->chunk(100, function ($users) {
    // Process the records...

    return false;
});
```

<!-- If you are updating database records while chunking results, your chunk results could change in unexpected ways. If you plan to update the retrieved records while chunking, it is always best to use the `chunkById` method instead. This method will automatically paginate the results based on the record's primary key: -->
청크 처리를 하면서 동시에 데이터베이스 레코드를 업데이트할 경우, 의도치 않게 참조 대상이 변경될 수 있습니다. 이처럼 청크 처리 중에 레코드를 수정할 계획이라면 `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 자동으로 기본 키를 기준으로 페이지네이션 처리하여 레코드를 나눕니다.

```
DB::table('users')->where('active', false)
    ->chunkById(100, function ($users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

> [!WARNING]
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 때, 기본 키 또는 외래 키의 변경은 청크 쿼리에 영향을 미칠 수 있습니다. 이로 인해 일부 레코드가 청크 결과에서 누락되는 등의 문제가 발생할 수 있습니다.

<a name="streaming-results-lazily"></a>
<!-- ### Streaming Results Lazily -->
### Streaming Results Lazily

<!-- The `lazy` method works similarly to [the `chunk` method](#chunking-results) in the sense that it executes the query in chunks. However, instead of passing each chunk into a callback, the `lazy()` method returns a [`LazyCollection`](/docs/9.x/collections#lazy-collections), which lets you interact with the results as a single stream: -->
`lazy` 메서드는 [the `chunk` method](#chunking-results)처럼 쿼리를 일정 단위로 실행한다는 점에서 유사하지만, 각 청크를 콜백으로 전달하는 대신 `lazy()` 메서드는 [`LazyCollection`](/docs/9.x/collections#lazy-collections) 인스턴스를 반환하여 데이터 스트림처럼 다룰 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

<!-- Once again, if you plan to update the retrieved records while iterating over them, it is best to use the `lazyById` or `lazyByIdDesc` methods instead. These methods will automatically paginate the results based on the record's primary key: -->
마찬가지로, 반복 도중에 조회한 레코드를 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드들은 레코드의 기본 키를 기준으로 자동으로 페이지네이션을 처리합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 도중에 레코드를 업데이트하거나 삭제할 경우, 기본 키 또는 외래 키의 변경은 청크 쿼리에 영향을 줄 수 있습니다. 그로 인해 일부 레코드가 결과에 포함되지 않을 수 있습니다.

<a name="aggregates"></a>
<!-- ### Aggregates -->
### Aggregates

<!-- The query builder also provides a variety of methods for retrieving aggregate values like `count`, `max`, `min`, `avg`, and `sum`. You may call any of these methods after constructing your query: -->
쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 과 같은 다양한 집계 함수 메서드를 제공합니다. 쿼리를 원하는 조건으로 작성한 뒤, 이러한 메서드를 호출할 수 있습니다.

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

<!-- Of course, you may combine these methods with other clauses to fine-tune how your aggregate value is calculated: -->
물론, 집계 메서드는 다른 조건과 함께 조합하여 더욱 세밀하게 원하는 값을 구할 수도 있습니다.

```
$price = DB::table('orders')
                ->where('finalized', 1)
                ->avg('price');
```

<a name="determining-if-records-exist"></a>
<!-- #### Determining If Records Exist -->
#### Determining If Records Exist

<!-- Instead of using the `count` method to determine if any records exist that match your query's constraints, you may use the `exists` and `doesntExist` methods: -->
쿼리의 조건에 맞는 레코드가 존재하는지 확인할 때 굳이 `count` 메서드를 쓸 필요 없이, `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다.

```
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
<!-- #### Specifying A Select Clause -->
#### Specifying A Select Clause

<!-- You may not always want to select all columns from a database table. Using the `select` method, you can specify a custom "select" clause for the query: -->
항상 테이블의 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용하면 쿼리의 "select" 절에 원하는 컬럼만을 지정할 수 있습니다.

```
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->select('name', 'email as user_email')
            ->get();
```

<!-- The `distinct` method allows you to force the query to return distinct results: -->
특정 컬럼의 중복을 제거하고 싶다면 `distinct` 메서드를 사용할 수 있습니다.

```
$users = DB::table('users')->distinct()->get();
```

<!-- If you already have a query builder instance and you wish to add a column to its existing select clause, you may use the `addSelect` method: -->
이미 쿼리 빌더 인스턴스를 가지고 있고, 기존 select 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용할 수 있습니다.

```
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
<!-- ## Raw Expressions -->
## Raw Expressions

<!-- Sometimes you may need to insert an arbitrary string into a query. To create a raw string expression, you may use the `raw` method provided by the `DB` facade: -->
때때로 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 이럴 때는 `DB` 파사드의 `raw` 메서드를 사용하여 Raw 문자열 표현식을 만들 수 있습니다.

```
$users = DB::table('users')
             ->select(DB::raw('count(*) as user_count, status'))
             ->where('status', '<>', 1)
             ->groupBy('status')
             ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열 그대로 삽입되므로 SQL 인젝션 취약점을 방지할 수 있도록 매우 주의해서 사용해야 합니다.

<a name="raw-methods"></a>
<!-- ### Raw Methods -->
### Raw Methods

<!-- Instead of using the `DB::raw` method, you may also use the following methods to insert a raw expression into various parts of your query. **Remember, Laravel can not guarantee that any query using raw expressions is protected against SQL injection vulnerabilities.** -->
`DB::raw` 대신, Raw 표현식을 쿼리의 다양한 부분에 삽입할 수 있는 다음 메서드들을 사용할 수도 있습니다.
**주의: Raw 표현식을 이용한 쿼리는 Laravel이 SQL 인젝션에 대한 보안을 완전히 보장할 수 없습니다.**

<a name="selectraw"></a>
<!-- #### `selectRaw` -->
#### `selectRaw`

<!-- The `selectRaw` method can be used in place of `addSelect(DB::raw(/* ... */))`. This method accepts an optional array of bindings as its second argument: -->
`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신에 사용할 수 있습니다. 두 번째 인자로 바인딩 배열을 옵션으로 전달할 수 있습니다.

```
$orders = DB::table('orders')
                ->selectRaw('price * ? as price_with_tax', [1.0825])
                ->get();
```

<a name="whereraw-orwhereraw"></a>
<!-- #### `whereRaw / orWhereRaw` -->
#### `whereRaw / orWhereRaw`

<!-- The `whereRaw` and `orWhereRaw` methods can be used to inject a raw "where" clause into your query. These methods accept an optional array of bindings as their second argument: -->
`whereRaw`와 `orWhereRaw` 메서드는 쿼리에 Raw "where" 절을 삽입할 때 사용합니다. 마찬가지로 두 번째 인자로 바인딩 배열을 옵션으로 전달할 수 있습니다.

```
$orders = DB::table('orders')
                ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                ->get();
```

<a name="havingraw-orhavingraw"></a>
<!-- #### `havingRaw / orHavingRaw` -->
#### `havingRaw / orHavingRaw`

<!-- The `havingRaw` and `orHavingRaw` methods may be used to provide a raw string as the value of the "having" clause. These methods accept an optional array of bindings as their second argument: -->
`havingRaw`와 `orHavingRaw` 메서드를 사용하면 "having" 절의 값으로 직접 Raw 문자열을 전달할 수 있습니다. 이 메서드들 역시 옵션으로 바인딩 배열을 두 번째 인자로 전달합니다.

```
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
`orderByRaw` 메서드를 사용하면 "order by" 절의 값으로 Raw 문자열을 전달할 수 있습니다.

```
$orders = DB::table('orders')
                ->orderByRaw('updated_at - created_at DESC')
                ->get();
```

<a name="groupbyraw"></a>
<!-- ### `groupByRaw` -->
### `groupByRaw`

<!-- The `groupByRaw` method may be used to provide a raw string as the value of the `group by` clause: -->
`groupByRaw` 메서드는 `group by` 절의 값으로 Raw 문자열을 지정할 때 사용합니다.

```
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
쿼리 빌더를 이용해 쿼리에 조인(join)절도 추가할 수 있습니다. 기본적인 "inner join"을 수행하려면 쿼리 빌더 인스턴스에 `join` 메서드를 사용하면 됩니다. `join` 메서드의 첫 번째 인자는 조인할 테이블 이름, 나머지 인자들은 조인 조건을 지정합니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다.

```
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
"inner join"이 아닌 "left join" 또는 "right join"을 하고 싶다면, `leftJoin` 또는 `rightJoin` 메서드를 사용할 수 있습니다. 이들 메서드의 시그니처는 `join`과 동일합니다.

```
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
"크로스 조인"을 수행하려면 `crossJoin` 메서드를 사용하세요. 크로스 조인은 첫 번째 테이블과 조인된 테이블의 카테시안 곱을 생성합니다.

```
$sizes = DB::table('sizes')
            ->crossJoin('colors')
            ->get();
```

<a name="advanced-join-clauses"></a>
<!-- #### Advanced Join Clauses -->
#### Advanced Join Clauses

<!-- You may also specify more advanced join clauses. To get started, pass a closure as the second argument to the `join` method. The closure will receive a `Illuminate\Database\Query\JoinClause` instance which allows you to specify constraints on the "join" clause: -->
더 복잡한 조인 절을 작성하고 싶다면, `join` 메서드의 두 번째 인자로 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아, 조인 조건을 더욱 세밀하게 지정할 수 있습니다.

```
DB::table('users')
        ->join('contacts', function ($join) {
            $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
        })
        ->get();
```

<!-- If you would like to use a "where" clause on your joins, you may use the `where` and `orWhere` methods provided by the `JoinClause` instance. Instead of comparing two columns, these methods will compare the column against a value: -->
조인에서 "where" 조건으로 값을 비교하고 싶다면, `JoinClause` 인스턴스가 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이 메서드들은 두 컬럼 간 비교가 아니라, 컬럼과 값의 비교를 수행합니다.

```
DB::table('users')
        ->join('contacts', function ($join) {
            $join->on('users.id', '=', 'contacts.user_id')
                 ->where('contacts.user_id', '>', 5);
        })
        ->get();
```

<a name="subquery-joins"></a>
<!-- #### Subquery Joins -->
#### Subquery Joins

<!-- You may use the `joinSub`, `leftJoinSub`, and `rightJoinSub` methods to join a query to a subquery. Each of these methods receives three arguments: the subquery, its table alias, and a closure that defines the related columns. In this example, we will retrieve a collection of users where each user record also contains the `created_at` timestamp of the user's most recently published blog post: -->
`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 쿼리를 서브쿼리와 조인할 수 있습니다. 각 메서드는 세 가지 인자를 받는데, 첫 번째는 서브쿼리, 두 번째는 테이블 별칭(alias), 세 번째는 관련 컬럼을 정의하는 클로저입니다. 아래 예제는 각 사용자 레코드에 해당 사용자의 최신 게시글의 `created_at` 타임스탬프를 함께 조회합니다.

```
$latestPosts = DB::table('posts')
                   ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
                   ->where('is_published', true)
                   ->groupBy('user_id');

$users = DB::table('users')
        ->joinSub($latestPosts, 'latest_posts', function ($join) {
            $join->on('users.id', '=', 'latest_posts.user_id');
        })->get();
```

<a name="unions"></a>
<!-- ## Unions -->
## Unions

<!-- The query builder also provides a convenient method to "union" two or more queries together. For example, you may create an initial query and use the `union` method to union it with more queries: -->
쿼리 빌더는 두 개 이상의 쿼리를 "유니온(union)"으로 합치는 편리한 메서드도 제공합니다. 예를 들어, 처음에 쿼리를 만들고, `union` 메서드를 이용해 다른 쿼리와 합칠 수 있습니다.

```
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
            ->whereNull('first_name');

$users = DB::table('users')
            ->whereNull('last_name')
            ->union($first)
            ->get();
```

<!-- In addition to the `union` method, the query builder provides a `unionAll` method. Queries that are combined using the `unionAll` method will not have their duplicate results removed. The `unionAll` method has the same method signature as the `union` method. -->
`union` 메서드 외에도, `unionAll` 메서드가 제공됩니다. `unionAll`로 합쳐진 쿼리의 결과는 중복 값이 제거되지 않으며, `unionAll` 메서드의 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
<!-- ## Basic Where Clauses -->
## Basic Where Clauses

<a name="where-clauses"></a>
<!-- ### Where Clauses -->
### Where Clauses

<!-- You may use the query builder's `where` method to add "where" clauses to the query. The most basic call to the `where` method requires three arguments. The first argument is the name of the column. The second argument is an operator, which can be any of the database's supported operators. The third argument is the value to compare against the column's value. -->
쿼리 빌더의 `where` 메서드를 사용하면 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 `where` 메서드 호출은 세 개의 인자를 받는데, 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 연산자), 세 번째는 컬럼과 비교할 값입니다.

<!-- For example, the following query retrieves users where the value of the `votes` column is equal to `100` and the value of the `age` column is greater than `35`: -->
아래 예제는 `votes` 컬럼이 `100`이고, `age` 컬럼이 `35`를 초과하는 사용자를 조회합니다.

```
$users = DB::table('users')
                ->where('votes', '=', 100)
                ->where('age', '>', 35)
                ->get();
```

<!-- For convenience, if you want to verify that a column is `=` to a given value, you may pass the value as the second argument to the `where` method. Laravel will assume you would like to use the `=` operator: -->
편의를 위해 컬럼이 `=`와 같은지 확인하고 싶다면, `where` 메서드의 두 번째 인자로 값을 바로 전달할 수 있습니다. Laravel은 내부적으로 `=` 연산자를 자동으로 사용합니다.

```
$users = DB::table('users')->where('votes', 100)->get();
```

<!-- As previously mentioned, you may use any operator that is supported by your database system: -->
이미 설명한 것처럼, 데이터베이스가 지원하는 어떤 연산자도 사용할 수 있습니다.

```
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
또한, 조건의 배열을 `where` 함수에 전달할 수 있습니다. 배열의 각 요소는 기본적으로 `where` 메서드에 전달되는 세 개의 인자가 하나의 배열로 담깁니다.

```
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 그러므로 쿼리에서 참조하는 컬럼명(특히 "order by" 컬럼 등)에 사용자의 입력값을 직접 반영해서는 안 됩니다.

<a name="or-where-clauses"></a>
<!-- ### Or Where Clauses -->
### Or Where Clauses

<!-- When chaining together calls to the query builder's `where` method, the "where" clauses will be joined together using the `and` operator. However, you may use the `orWhere` method to join a clause to the query using the `or` operator. The `orWhere` method accepts the same arguments as the `where` method: -->
여러 개의 `where` 메서드를 체이닝하면, 조건들은 `and` 연산자로 연결됩니다. 하지만, `or`로 조건을 연결하려면 `orWhere` 메서드를 사용하면 됩니다. `orWhere`는 `where`와 동일한 인자를 받습니다.

```
$users = DB::table('users')
                    ->where('votes', '>', 100)
                    ->orWhere('name', 'John')
                    ->get();
```

<!-- If you need to group an "or" condition within parentheses, you may pass a closure as the first argument to the `orWhere` method: -->
만약 or 조건을 괄호로 묶어 그룹화해야 한다면, `orWhere` 메서드의 첫 번째 인자로 클로저를 전달할 수 있습니다.

```
$users = DB::table('users')
            ->where('votes', '>', 100)
            ->orWhere(function($query) {
                $query->where('name', 'Abigail')
                      ->where('votes', '>', 50);
            })
            ->get();
```

<!-- The example above will produce the following SQL: -->
위 코드는 아래와 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 예기치 않은 동작을 방지하기 위해, `orWhere`를 사용할 때는 반드시 괄호로 묶어 그룹을 지어야 합니다. 글로벌 스코프가 적용된 경우 특히 주의가 필요합니다.

<a name="where-not-clauses"></a>
<!-- ### Where Not Clauses -->
### Where Not Clauses

<!-- The `whereNot` and `orWhereNot` methods may be used to negate a given group of query constraints. For example, the following query excludes products that are on clearance or which have a price that is less than ten: -->
`whereNot`과 `orWhereNot` 메서드는 지정한 조건 그룹을 부정(negate)하는 데 사용할 수 있습니다. 예를 들어, 아래 쿼리는 세일 품목이거나 가격이 10 미만인 상품을 결과에서 제외합니다.

```
$products = DB::table('products')
                ->whereNot(function ($query) {
                    $query->where('clearance', true)
                          ->orWhere('price', '<', 10);
                })
                ->get();
```

<a name="json-where-clauses"></a>
<!-- ### JSON Where Clauses -->
### JSON Where Clauses

<!-- Laravel also supports querying JSON column types on databases that provide support for JSON column types. Currently, this includes MySQL 5.7+, PostgreSQL, SQL Server 2016, and SQLite 3.39.0 (with the [JSON1 extension](https://www.sqlite.org/json1.html)). To query a JSON column, use the `->` operator: -->
Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MySQL 5.7+, PostgreSQL, SQL Server 2016, SQLite 3.39.0 이상(및 [JSON1 extension](https://www.sqlite.org/json1.html) 설치 필요))에서 JSON 컬럼에 대한 쿼리도 지원합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용하면 됩니다.

```
$users = DB::table('users')
                ->where('preferences->dining->meal', 'salad')
                ->get();
```

<!-- You may use `whereJsonContains` to query JSON arrays. This feature is not supported by SQLite database versions less than 3.38.0: -->
JSON 배열 내 값을 쿼리하려면 `whereJsonContains`를 사용할 수 있습니다. 이 기능은 SQLite 3.38.0 미만 버전에서는 지원되지 않습니다.

```
$users = DB::table('users')
                ->whereJsonContains('options->languages', 'en')
                ->get();
```

<!-- If your application uses the MySQL or PostgreSQL databases, you may pass an array of values to the `whereJsonContains` method: -->
애플리케이션에서 MySQL 또는 PostgreSQL을 사용한다면, `whereJsonContains`에 값의 배열도 전달할 수 있습니다.

```
$users = DB::table('users')
                ->whereJsonContains('options->languages', ['en', 'de'])
                ->get();
```

<!-- You may use `whereJsonLength` method to query JSON arrays by their length: -->
JSON 배열의 길이를 조건으로 쿼리하려면 `whereJsonLength` 메서드를 사용할 수 있습니다.

```
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

<!-- **whereBetween / orWhereBetween** -->
**whereBetween / orWhereBetween**

<!-- The `whereBetween` method verifies that a column's value is between two values: -->
`whereBetween` 메서드는 특정 컬럼의 값이 두 값 사이에 있는지 확인합니다.

```
$users = DB::table('users')
           ->whereBetween('votes', [1, 100])
           ->get();
```

<!-- **whereNotBetween / orWhereNotBetween** -->
**whereNotBetween / orWhereNotBetween**

<!-- The `whereNotBetween` method verifies that a column's value lies outside of two values: -->
`whereNotBetween` 메서드는 특정 컬럼의 값이 두 값의 범위 밖에 있는지 확인합니다.

```
$users = DB::table('users')
                    ->whereNotBetween('votes', [1, 100])
                    ->get();
```

<!-- **whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns** -->
**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

<!-- The `whereBetweenColumns` method verifies that a column's value is between the two values of two columns in the same table row: -->
`whereBetweenColumns` 메서드는 해당 행에서 두 컬럼의 값 사이에 특정 컬럼의 값이 포함되는지 확인합니다.

```
$patients = DB::table('patients')
                       ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

<!-- The `whereNotBetweenColumns` method verifies that a column's value lies outside the two values of two columns in the same table row: -->
`whereNotBetweenColumns` 메서드는 해당 행에서 두 컬럼의 값의 범위 밖에 특정 컬럼의 값이 있는지 확인합니다.

```
$patients = DB::table('patients')
                       ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

<!-- **whereIn / whereNotIn / orWhereIn / orWhereNotIn** -->
**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

<!-- The `whereIn` method verifies that a given column's value is contained within the given array: -->
`whereIn` 메서드는 주어진 컬럼의 값이 지정한 배열 안에 포함되어 있는지 확인합니다.

```
$users = DB::table('users')
                    ->whereIn('id', [1, 2, 3])
                    ->get();
```

<!-- The `whereNotIn` method verifies that the given column's value is not contained in the given array: -->
`whereNotIn` 메서드는 주어진 컬럼의 값이 해당 배열에 포함되어 있지 않은지 확인합니다.

```
$users = DB::table('users')
                    ->whereNotIn('id', [1, 2, 3])
                    ->get();
```

<!-- You may also provide a query object as the `whereIn` method's second argument: -->
또한 `whereIn` 메서드의 두 번째 인수로 쿼리 객체를 전달할 수도 있습니다.

```
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
                    ->whereIn('user_id', $activeUsers)
                    ->get();
```

<!-- The example above will produce the following SQL: -->
위 예시 코드에서 생성되는 SQL은 다음과 같습니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 많은 수의 정수로 이루어진 배열을 바인딩해야 할 때, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

<!-- **whereNull / whereNotNull / orWhereNull / orWhereNotNull** -->
**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

<!-- The `whereNull` method verifies that the value of the given column is `NULL`: -->
`whereNull` 메서드는 주어진 컬럼의 값이 `NULL`인지 확인합니다.

```
$users = DB::table('users')
                ->whereNull('updated_at')
                ->get();
```

<!-- The `whereNotNull` method verifies that the column's value is not `NULL`: -->
`whereNotNull` 메서드는 해당 컬럼의 값이 `NULL`이 아닌지 확인합니다.

```
$users = DB::table('users')
                ->whereNotNull('updated_at')
                ->get();
```

<!-- **whereDate / whereMonth / whereDay / whereYear / whereTime** -->
**whereDate / whereMonth / whereDay / whereYear / whereTime**

<!-- The `whereDate` method may be used to compare a column's value against a date: -->
`whereDate` 메서드는 컬럼의 값을 특정 날짜와 비교할 수 있습니다.

```
$users = DB::table('users')
                ->whereDate('created_at', '2016-12-31')
                ->get();
```

<!-- The `whereMonth` method may be used to compare a column's value against a specific month: -->
`whereMonth` 메서드는 컬럼의 값을 특정 월과 비교할 때 사용합니다.

```
$users = DB::table('users')
                ->whereMonth('created_at', '12')
                ->get();
```

<!-- The `whereDay` method may be used to compare a column's value against a specific day of the month: -->
`whereDay` 메서드는 컬럼의 값을 달의 특정 일(day)과 비교할 때 사용합니다.

```
$users = DB::table('users')
                ->whereDay('created_at', '31')
                ->get();
```

<!-- The `whereYear` method may be used to compare a column's value against a specific year: -->
`whereYear` 메서드는 컬럼의 값을 특정 연도와 비교할 때 사용합니다.

```
$users = DB::table('users')
                ->whereYear('created_at', '2016')
                ->get();
```

<!-- The `whereTime` method may be used to compare a column's value against a specific time: -->
`whereTime` 메서드는 컬럼의 값을 특정 시간과 비교할 때 사용합니다.

```
$users = DB::table('users')
                ->whereTime('created_at', '=', '11:20:45')
                ->get();
```

<!-- **whereColumn / orWhereColumn** -->
**whereColumn / orWhereColumn**

<!-- The `whereColumn` method may be used to verify that two columns are equal: -->
`whereColumn` 메서드는 두 컬럼의 값이 같은지 비교하는 데 사용할 수 있습니다.

```
$users = DB::table('users')
                ->whereColumn('first_name', 'last_name')
                ->get();
```

<!-- You may also pass a comparison operator to the `whereColumn` method: -->
`whereColumn` 메서드에 비교 연산자를 함께 전달하여 사용할 수도 있습니다.

```
$users = DB::table('users')
                ->whereColumn('updated_at', '>', 'created_at')
                ->get();
```

<!-- You may also pass an array of column comparisons to the `whereColumn` method. These conditions will be joined using the `and` operator: -->
또한 `whereColumn` 메서드에 여러 컬럼 비교를 위한 배열을 전달할 수 있습니다. 이 조건들은 모두 `and` 연산자로 연결됩니다.

```
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
쿼리에서 원하는 논리적인 그룹화를 만들기 위해 여러 개의 "where" 절을 괄호로 묶어야 할 때가 있습니다. 특히, `orWhere` 메서드를 사용할 때는 원하지 않는 쿼리 동작을 방지하기 위해 항상 괄호로 묶어주는 것이 좋습니다. 이를 위해 `where` 메서드에 클로저를 전달할 수 있습니다.

```
$users = DB::table('users')
           ->where('name', '=', 'John')
           ->where(function ($query) {
               $query->where('votes', '>', 100)
                     ->orWhere('title', '=', 'Admin');
           })
           ->get();
```

<!-- As you can see, passing a closure into the `where` method instructs the query builder to begin a constraint group. The closure will receive a query builder instance which you can use to set the constraints that should be contained within the parenthesis group. The example above will produce the following SQL: -->
이처럼, `where` 메서드에 클로저를 전달하면 쿼리 빌더는 괄호 그룹을 시작하게 됩니다. 클로저에는 쿼리 빌더 인스턴스가 전달되며, 괄호 그룹 내에 포함시킬 조건을 정의할 수 있습니다. 위의 예시 코드는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해 `orWhere` 호출은 항상 묶어주는 습관을 들이세요.

<a name="advanced-where-clauses"></a>
<!-- ### Advanced Where Clauses -->
### Advanced Where Clauses

<a name="where-exists-clauses"></a>
<!-- ### Where Exists Clauses -->
### Where Exists Clauses

<!-- The `whereExists` method allows you to write "where exists" SQL clauses. The `whereExists` method accepts a closure which will receive a query builder instance, allowing you to define the query that should be placed inside of the "exists" clause: -->
`whereExists` 메서드는 "where exists" SQL 절을 쓸 수 있게 해줍니다. `whereExists` 메서드는 클로저를 인수로 받아서, 클로저 내에서 "exists" 절 안에 들어갈 쿼리를 정의할 수 있습니다.

```
$users = DB::table('users')
           ->whereExists(function ($query) {
               $query->select(DB::raw(1))
                     ->from('orders')
                     ->whereColumn('orders.user_id', 'users.id');
           })
           ->get();
```

<!-- The query above will produce the following SQL: -->
위 쿼리는 다음과 같은 SQL을 생성합니다.

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
때로는 서브쿼리의 결과와 특정 값을 비교하는 "where" 절이 필요할 수 있습니다. 이 경우, `where` 메서드에 클로저와 값을 함께 전달하면 됩니다. 예를 들어, 다음 쿼리는 특정 타입의 최근 "membership"을 가진 모든 사용자를 가져옵니다.

```
use App\Models\User;

$users = User::where(function ($query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

<!-- Or, you may need to construct a "where" clause that compares a column to the results of a subquery. You may accomplish this by passing a column, operator, and closure to the `where` method. For example, the following query will retrieve all income records where the amount is less than average; -->
또 다른 예로, 컬럼 값을 서브쿼리의 결과와 비교하고 싶다면, 컬럼명, 연산자, 클로저를 `where` 메서드에 전달하면 됩니다. 다음 쿼리는 수입(income) 기록 중 금액이 평균보다 작은 모든 레코드를 조회합니다.

```
use App\Models\Income;

$incomes = Income::where('amount', '<', function ($query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
<!-- ### Full Text Where Clauses -->
### Full Text Where Clauses

> [!WARNING]
> 전문(Full Text) where 절은 현재 MySQL과 PostgreSQL에서만 지원됩니다.

<!-- The `whereFullText` and `orWhereFullText` methods may be used to add full text "where" clauses to a query for columns that have [full text indexes](/docs/9.x/migrations#available-index-types). These methods will be transformed into the appropriate SQL for the underlying database system by Laravel. For example, a `MATCH AGAINST` clause will be generated for applications utilizing MySQL: -->
`whereFullText` 및 `orWhereFullText` 메서드는 [full text indexes](/docs/9.x/migrations#available-index-types)가 설정되어 있는 컬럼에 대해 전문 "where" 절을 쿼리에 추가할 수 있습니다. 이 메서드들은 실제 데이터베이스에 맞게 적절한 SQL로 변환됩니다. 예를 들어 MySQL을 사용할 경우 `MATCH AGAINST` 절이 생성됩니다.

```
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
<!-- ## Ordering, Grouping, Limit & Offset -->
## Ordering, Grouping, Limit & Offset

<a name="ordering"></a>
<!-- ### Ordering -->
### Ordering

<a name="orderby"></a>
<!-- #### The `orderBy` Method -->
#### The `orderBy` Method

<!-- The `orderBy` method allows you to sort the results of the query by a given column. The first argument accepted by the `orderBy` method should be the column you wish to sort by, while the second argument determines the direction of the sort and may be either `asc` or `desc`: -->
`orderBy` 메서드는 쿼리 결과를 지정한 컬럼 기준으로 정렬할 수 있게 해줍니다. `orderBy` 메서드의 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)을 지정합니다.

```
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->get();
```

<!-- To sort by multiple columns, you may simply invoke `orderBy` as many times as necessary: -->
여러 컬럼 기준으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다.

```
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->orderBy('email', 'asc')
                ->get();
```

<a name="latest-oldest"></a>
<!-- #### The `latest` & `oldest` Methods -->
#### The `latest` & `oldest` Methods

<!-- The `latest` and `oldest` methods allow you to easily order results by date. By default, the result will be ordered by the table's `created_at` column. Or, you may pass the column name that you wish to sort by: -->
`latest` 및 `oldest` 메서드를 사용하면 날짜 기준으로 쉽게 결과를 정렬할 수 있습니다. 기본적으로 테이블의 `created_at` 컬럼을 기준으로 정렬됩니다. 원하는 컬럼명을 직접 지정할 수도 있습니다.

```
$user = DB::table('users')
                ->latest()
                ->first();
```

<a name="random-ordering"></a>
<!-- #### Random Ordering -->
#### Random Ordering

<!-- The `inRandomOrder` method may be used to sort the query results randomly. For example, you may use this method to fetch a random user: -->
`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 임의의 사용자를 반환할때 활용할 수 있습니다.

```
$randomUser = DB::table('users')
                ->inRandomOrder()
                ->first();
```

<a name="removing-existing-orderings"></a>
<!-- #### Removing Existing Orderings -->
#### Removing Existing Orderings

<!-- The `reorder` method removes all of the "order by" clauses that have previously been applied to the query: -->
`reorder` 메서드는 쿼리에 적용되어 있던 모든 "order by" 절을 제거합니다.

```
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

<!-- You may pass a column and direction when calling the `reorder` method in order to remove all existing "order by" clauses and apply an entirely new order to the query: -->
`reorder` 메서드 호출 시 컬럼명과 정렬 방향을 전달하면 기존의 모든 "order by" 를 제거하고 새로운 기준으로 정렬할 수 있습니다.

```
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
<!-- ### Grouping -->
### Grouping

<a name="groupby-having"></a>
<!-- #### The `groupBy` & `having` Methods -->
#### The `groupBy` & `having` Methods

<!-- As you might expect, the `groupBy` and `having` methods may be used to group the query results. The `having` method's signature is similar to that of the `where` method: -->
예상하셨겠지만, `groupBy`와 `having` 메서드를 이용하여 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드의 시그니처는 `where`와 유사합니다.

```
$users = DB::table('users')
                ->groupBy('account_id')
                ->having('account_id', '>', 100)
                ->get();
```

<!-- You can use the `havingBetween` method to filter the results within a given range: -->
결과를 특정 범위로 필터링하고 싶을 때에는 `havingBetween` 메서드를 사용할 수 있습니다.

```
$report = DB::table('orders')
                ->selectRaw('count(id) as number_of_orders, customer_id')
                ->groupBy('customer_id')
                ->havingBetween('number_of_orders', [5, 15])
                ->get();
```

<!-- You may pass multiple arguments to the `groupBy` method to group by multiple columns: -->
`groupBy` 메서드에 여러 인수를 전달하여 여러 컬럼 기준으로 그룹화할 수도 있습니다.

```
$users = DB::table('users')
                ->groupBy('first_name', 'status')
                ->having('account_id', '>', 100)
                ->get();
```

<!-- To build more advanced `having` statements, see the [`havingRaw`](#raw-methods) method. -->
보다 고급의 `having` 구문을 작성하려면 [`havingRaw`](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
<!-- ### Limit & Offset -->
### Limit & Offset

<a name="skip-take"></a>
<!-- #### The `skip` & `take` Methods -->
#### The `skip` & `take` Methods

<!-- You may use the `skip` and `take` methods to limit the number of results returned from the query or to skip a given number of results in the query: -->
`skip` 및 `take` 메서드를 사용하면 결과의 시작 위치(오프셋)와 반한 개수를 제한할 수 있습니다.

```
$users = DB::table('users')->skip(10)->take(5)->get();
```

<!-- Alternatively, you may use the `limit` and `offset` methods. These methods are functionally equivalent to the `take` and `skip` methods, respectively: -->
다른 방법으로, `limit`과 `offset` 메서드도 사용할 수 있습니다. 이 두 메서드는 각각 `take` 및 `skip`과 동일한 기능을 합니다.

```
$users = DB::table('users')
                ->offset(10)
                ->limit(5)
                ->get();
```

<a name="conditional-clauses"></a>
<!-- ## Conditional Clauses -->
## Conditional Clauses

<!-- Sometimes you may want certain query clauses to apply to a query based on another condition. For instance, you may only want to apply a `where` statement if a given input value is present on the incoming HTTP request. You may accomplish this using the `when` method: -->
특정 조건에 따라 쿼리에 일부 절만 적용하고 싶을 때가 있습니다. 예를 들어, 입력값이 있을 때만 `where` 구문을 적용하고 싶을 수 있습니다. 이럴 때는 `when` 메서드를 사용하세요.

```
$role = $request->input('role');

$users = DB::table('users')
                ->when($role, function ($query, $role) {
                    $query->where('role_id', $role);
                })
                ->get();
```

<!-- The `when` method only executes the given closure when the first argument is `true`. If the first argument is `false`, the closure will not be executed. So, in the example above, the closure given to the `when` method will only be invoked if the `role` field is present on the incoming request and evaluates to `true`. -->
`when` 메서드는 첫 번째 인수(condition)가 `true`일 때만 전달된 클로저를 실행합니다. `false`면 클로저는 실행되지 않습니다. 위 예시에서는, 요청에 `role` 필드가 존재하고 값이 `true`일 때만 `when` 메서드에 전달된 클로저가 실행되어 쿼리에 조건이 추가됩니다.

<!-- You may pass another closure as the third argument to the `when` method. This closure will only execute if the first argument evaluates as `false`. To illustrate how this feature may be used, we will use it to configure the default ordering of a query: -->
또한 `when` 메서드의 세 번째 인수로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 첫 번째 인수가 `false`일 때 실행됩니다. 이 기능을 활용해 쿼리의 기본 정렬 방식을 지정할 수 있습니다.

```
$sortByVotes = $request->input('sort_by_votes');

$users = DB::table('users')
                ->when($sortByVotes, function ($query, $sortByVotes) {
                    $query->orderBy('votes');
                }, function ($query) {
                    $query->orderBy('name');
                })
                ->get();
```

<a name="insert-statements"></a>
<!-- ## Insert Statements -->
## Insert Statements

<!-- The query builder also provides an `insert` method that may be used to insert records into the database table. The `insert` method accepts an array of column names and values: -->
쿼리 빌더는 테이블에 레코드를 추가할 때 사용할 수 있는 `insert` 메서드도 제공합니다. `insert` 메서드는 컬럼명과 값을 갖는 배열을 인수로 받습니다.

```
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

<!-- You may insert several records at once by passing an array of arrays. Each array represents a record that should be inserted into the table: -->
여러 레코드를 한 번에 추가하려면, 배열의 배열을 전달하면 됩니다. 각 배열은 하나의 레코드를 의미합니다.

```
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

<!-- The `insertOrIgnore` method will ignore errors while inserting records into the database. When using this method, you should be aware that duplicate record errors will be ignored and other types of errors may also be ignored depending on the database engine. For example, `insertOrIgnore` will [bypass MySQL's strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution): -->
`insertOrIgnore` 메서드는 레코드를 추가하는 중에 발생하는 일부 에러를 무시합니다. 이 메서드를 사용할 때는 중복 레코드 오류는 무시되며 그 밖의 다른 오류도 데이터베이스 엔진에 따라 무시될 수 있다는 점에 유의해야 합니다. 예를 들어, `insertOrIgnore`는 [bypass MySQL's strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

<!-- The `insertUsing` method will insert new records into the table while using a subquery to determine the data that should be inserted: -->
`insertUsing` 메서드는 서브쿼리에서 조회한 데이터를 이용해 새로운 레코드를 테이블에 추가할 수 있습니다.

```
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
<!-- #### Auto-Incrementing IDs -->
#### Auto-Incrementing IDs

<!-- If the table has an auto-incrementing id, use the `insertGetId` method to insert a record and then retrieve the ID: -->
테이블에 자동 증가되는 id 컬럼이 있다면, `insertGetId` 메서드를 사용하여 레코드를 추가하면서 생성된 ID 값을 바로 받아올 수 있습니다.

```
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서 `insertGetId` 메서드를 사용할 경우, 자동 증가 컬럼명이 반드시 `id`여야 합니다. 만약 다른 "시퀀스"에서 ID 값을 얻고 싶다면, 해당 컬럼명을 `insertGetId` 메서드의 두 번째 인수로 넘길 수 있습니다.

<a name="upserts"></a>
<!-- ### Upserts -->
### Upserts

<!-- The `upsert` method will insert records that do not exist and update the records that already exist with new values that you may specify. The method's first argument consists of the values to insert or update, while the second argument lists the column(s) that uniquely identify records within the associated table. The method's third and final argument is an array of columns that should be updated if a matching record already exists in the database: -->
`upsert` 메서드는 존재하지 않는 레코드는 추가하고, 이미 존재하는 레코드는 새로운 값으로 갱신(업데이트)합니다. 첫 번째 인수로는 삽입 또는 업데이트할 값들을, 두 번째 인수에는 해당 테이블에서 레코드를 고유하게 식별할 컬럼(들)을 배열로, 세 번째 인수에는 레코드가 이미 존재할 경우 업데이트할 컬럼(들)을 배열로 전달합니다.

```
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
위 예시에서, Laravel은 두 개의 레코드를 추가 시도합니다. 만약 `departure`와 `destination` 컬럼이 동일한 레코드가 이미 존재하면, 해당 레코드의 `price` 컬럼만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수로 넘긴 컬럼에 "primary" 또는 "unique" 인덱스가 있어야 합니다. 또한, MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하고, 테이블의 "primary" 및 "unique" 인덱스를 이용해 기존 레코드를 판단합니다.

<a name="update-statements"></a>
<!-- ## Update Statements -->
## Update Statements

<!-- In addition to inserting records into the database, the query builder can also update existing records using the `update` method. The `update` method, like the `insert` method, accepts an array of column and value pairs indicating the columns to be updated. The `update` method returns the number of affected rows. You may constrain the `update` query using `where` clauses: -->
레코드를 추가(insert)하는 것 외에도, 쿼리 빌더를 통해 기존 레코드를 `update` 메서드로 수정할 수도 있습니다. `update` 메서드는 `insert`와 마찬가지로 컬럼과 값이 쌍으로 들어있는 배열을 인수로 받고, `update` 메서드는 영향받은 행(row)의 개수를 반환합니다. `where` 절을 이용해 `update` 쿼리의 대상을 제한할 수 있습니다.

```
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
<!-- #### Update Or Insert -->
#### Update Or Insert

<!-- Sometimes you may want to update an existing record in the database or create it if no matching record exists. In this scenario, the `updateOrInsert` method may be used. The `updateOrInsert` method accepts two arguments: an array of conditions by which to find the record, and an array of column and value pairs indicating the columns to be updated. -->
때로는 DB에서 특정 조건을 만족하는 레코드가 있으면 업데이트하고, 없다면 새로 추가해야 할 때가 있습니다. 이럴 때는 `updateOrInsert` 메서드를 사용할 수 있습니다. `updateOrInsert` 메서드는 두 개의 인수를 받는데, 첫 번째는 레코드를 찾을 조건을, 두 번째는 업데이트할 컬럼과 값의 배열입니다.

<!-- The `updateOrInsert` method will attempt to locate a matching database record using the first argument's column and value pairs. If the record exists, it will be updated with the values in the second argument. If the record can not be found, a new record will be inserted with the merged attributes of both arguments: -->
`updateOrInsert`는 첫 번째 조건에 맞는 레코드를 찾으려고 시도합니다. 있으면 두 번째 인수의 값으로 업데이트하고, 없으면 두 인수를 합친 속성으로 새 레코드를 추가합니다.

```
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<a name="updating-json-columns"></a>
<!-- ### Updating JSON Columns -->
### Updating JSON Columns

<!-- When updating a JSON column, you should use `->` syntax to update the appropriate key in the JSON object. This operation is supported on MySQL 5.7+ and PostgreSQL 9.5+: -->
JSON 컬럼을 업데이트할 때는 `->` 표기법을 사용하여 JSON 객체 안의 특정 키를 업데이트할 수 있습니다. 이 기능은 MySQL 5.7+ 또는 PostgreSQL 9.5+에서 지원합니다.

```
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
<!-- ### Increment & Decrement -->
### Increment & Decrement

<!-- The query builder also provides convenient methods for incrementing or decrementing the value of a given column. Both of these methods accept at least one argument: the column to modify. A second argument may be provided to specify the amount by which the column should be incremented or decremented: -->
쿼리 빌더는 지정한 컬럼의 값을 증가시키거나 감소시키는 메서드도 제공합니다. 이 두 메서드는 최소한 하나의 인수(대상 컬럼명)를 받으며, 두 번째 인수로 값의 증가 또는 감소량을 지정할 수 있습니다.

```
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

<!-- If needed, you may also specify additional columns to update during the increment or decrement operation: -->
필요하다면, 증가 또는 감소 연산과 동시에 추가적으로 다른 컬럼도 수정할 수 있습니다.

```
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

<!-- In addition, you may increment or decrement multiple columns at once using the `incrementEach` and `decrementEach` methods: -->
또한 `incrementEach`와 `decrementEach` 메서드를 이용하여 여러 컬럼을 한 번에 증가 또는 감소시킬 수 있습니다.

```
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>

<!-- ## Delete Statements -->
## Delete Statements

<!-- The query builder's `delete` method may be used to delete records from the table. The `delete` method returns the number of affected rows. You may constrain `delete` statements by adding "where" clauses before calling the `delete` method: -->
쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제할 때 사용할 수 있습니다. `delete` 메서드는 영향을 받은 행(row)의 개수를 반환합니다. `delete` 메서드를 호출하기 전에 "where" 절을 추가하여 `delete` 구문의 삭제 대상을 제한할 수도 있습니다.

```
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<!-- If you wish to truncate an entire table, which will remove all records from the table and reset the auto-incrementing ID to zero, you may use the `truncate` method: -->
만약 전체 테이블의 모든 레코드를 삭제하고, 자동 증가 ID도 0으로 초기화하고 싶다면, `truncate` 메서드를 사용할 수 있습니다.

```
DB::table('users')->truncate();
```

<a name="table-truncation-and-postgresql"></a>
<!-- #### Table Truncation & PostgreSQL -->
#### Table Truncation & PostgreSQL

<!-- When truncating a PostgreSQL database, the `CASCADE` behavior will be applied. This means that all foreign key related records in other tables will be deleted as well. -->
PostgreSQL 데이터베이스에서 트렁케이트(truncate) 작업을 수행하면, `CASCADE` 동작이 적용됩니다. 즉, 다른 테이블과 외래 키로 연관된 모든 레코드도 함께 삭제됩니다.

<a name="pessimistic-locking"></a>
<!-- ## Pessimistic Locking -->
## Pessimistic Locking

<!-- The query builder also includes a few functions to help you achieve "pessimistic locking" when executing your `select` statements. To execute a statement with a "shared lock", you may call the `sharedLock` method. A shared lock prevents the selected rows from being modified until your transaction is committed: -->
쿼리 빌더에는 `select` 문을 실행할 때 "비관적 잠금"을 적용할 수 있는 여러 메서드가 포함되어 있습니다. "공유 잠금(shared lock)"을 적용하여 쿼리를 실행하고자 한다면 `sharedLock` 메서드를 사용할 수 있습니다. 공유 잠금은 트랜잭션이 커밋될 때까지 선택된 행들이 수정되지 않도록 보호합니다.

```
DB::table('users')
        ->where('votes', '>', 100)
        ->sharedLock()
        ->get();
```

<!-- Alternatively, you may use the `lockForUpdate` method. A "for update" lock prevents the selected records from being modified or from being selected with another shared lock: -->
또는, `lockForUpdate` 메서드를 사용할 수도 있습니다. "for update" 잠금은 선택된 레코드가 수정되거나, 다른 트랜잭션에서 공유 잠금으로 선택되는 것을 모두 막아줍니다.

```
DB::table('users')
        ->where('votes', '>', 100)
        ->lockForUpdate()
        ->get();
```

<a name="debugging"></a>
<!-- ## Debugging -->
## Debugging

<!-- You may use the `dd` and `dump` methods while building a query to dump the current query bindings and SQL. The `dd` method will display the debug information and then stop executing the request. The `dump` method will display the debug information but allow the request to continue executing: -->
쿼리를 작성하는 동안, `dd` 및 `dump` 메서드를 사용해 현재 쿼리 바인딩과 SQL을 출력해 볼 수 있습니다. `dd` 메서드는 디버그 정보를 화면에 출력하고, 코드 실행을 즉시 중단합니다. 반면, `dump` 메서드는 디버그 정보만 출력하고 요청 처리는 계속 진행됩니다.

```
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```
