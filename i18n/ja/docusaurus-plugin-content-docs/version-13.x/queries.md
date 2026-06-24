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
Laravel のデータベース クエリビルダは、データベース クエリを作成および実行するための便利で流暢なインターフェイスを提供します。これはアプリケーションでほとんどのデータベース操作を実行するために使用でき、Laravel でサポートされているすべてのデータベース システムと完全に連携します。

<!-- The Laravel query builder uses PDO parameter binding to protect your application against SQL injection attacks. There is no need to clean or sanitize strings passed to the query builder as query bindings. -->
Laravel クエリビルダは、PDO パラメーター バインディングを使用して、アプリケーションを SQL インジェクション攻撃から保護します。クエリ バインディングとしてクエリビルダに渡される文字列をクリーンアップまたはサニタイズする必要はありません。

> [!WARNING]
> PDO は列名のバインドをサポートしていません。したがって、「order by」列を含め、クエリで参照される列名をユーザー入力によって決定することを決して許可しないでください。

<a name="running-database-queries"></a>
<!-- ## Running Database Queries -->
## Running Database Queries

<a name="retrieving-all-rows-from-a-table"></a>
<!-- #### Retrieving All Rows From a Table -->
#### Retrieving All Rows From a Table

<!-- You may use the `table` method provided by the `DB` facade to begin a query. The `table` method returns a fluent query builder instance for the given table, allowing you to chain more constraints onto the query and then finally retrieve the results of the query using the `get` method: -->
`DB` ファサードによって提供される `table` メソッドを使用して、クエリを開始できます。 `table` メソッドは、指定されたテーブルの流暢なクエリビルダ インスタンスを返します。これにより、クエリにさらに多くの制約を連鎖させ、最後に `get` メソッドを使用してクエリの結果を取得できます。

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
`get` メソッドは、クエリの結果を含む `Illuminate\Support\Collection` インスタンスを返します。各結果は PHP `stdClass` オブジェクトのインスタンスです。オブジェクトのプロパティとして列にアクセスすることで、各列の値にアクセスできます。

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel コレクションは、データのマッピングと削減のための非常に強力なさまざまな方法を提供します。 Laravel コレクションの詳細については、[collection documentation](/docs/13.x/collections) をチェックしてください。

<a name="retrieving-a-single-row-column-from-a-table"></a>
<!-- #### Retrieving a Single Row / Column From a Table -->
#### Retrieving a Single Row / Column From a Table

<!-- If you just need to retrieve a single row from a database table, you may use the `DB` facade's `first` method. This method will return a single `stdClass` object: -->
データベース テーブルから 1 つの行を取得するだけの場合は、`DB` ファサードの `first` メソッドを使用できます。このメソッドは、単一の `stdClass` オブジェクトを返します。

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

<!-- If you would like to retrieve a single row from a database table, but throw an `Illuminate\Database\RecordNotFoundException` if no matching row is found, you may use the `firstOrFail` method. If the `RecordNotFoundException` is not caught, a 404 HTTP response is automatically sent back to the client: -->
データベーステーブルから単一行を取得したいが、一致する行が見つからない場合は `Illuminate\Database\RecordNotFoundException` をスローする場合は、`firstOrFail` メソッドを使用できます。 `RecordNotFoundException` が捕捉されない場合、404 HTTP 応答が自動的にクライアントに返されます。

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

<!-- If you don't need an entire row, you may extract a single value from a record using the `value` method. This method will return the value of the column directly: -->
行全体が必要ない場合は、`value` メソッドを使用してレコードから単一の値を抽出できます。このメソッドは列の値を直接返します。

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

<!-- To retrieve a single row by its `id` column value, use the `find` method: -->
`id` 列の値によって単一行を取得するには、`find` メソッドを使用します。

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
<!-- #### Retrieving a List of Column Values -->
#### Retrieving a List of Column Values

<!-- If you would like to retrieve an `Illuminate\Support\Collection` instance containing the values of a single column, you may use the `pluck` method. In this example, we'll retrieve a collection of user titles: -->
単一列の値を含む `Illuminate\Support\Collection` インスタンスを取得したい場合は、`pluck` メソッドを使用できます。この例では、ユーザーのタイトルのコレクションを取得します。

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

<!-- You may specify the column that the resulting collection should use as its keys by providing a second argument to the `pluck` method: -->
`pluck` メソッドに 2 番目の引数を指定することで、結果のコレクションがキーとして使用する列を指定できます。

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
数千のデータベース レコードを操作する必要がある場合は、`DB` ファサードによって提供される `chunk` メソッドの使用を検討してください。このメソッドは、一度に結果の小さなチャンクを取得し、各チャンクを処理のためにクロージャにフィードします。たとえば、`users` テーブル全体を一度に 100 レコードずつ取得してみましょう。

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
クロージャから `false` を返すことで、それ以上のチャンクの処理を停止できます。

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```

<!-- If you are updating database records while chunking results, your chunk results could change in unexpected ways. If you plan to update the retrieved records while chunking, it is always best to use the `chunkById` method instead. This method will automatically paginate the results based on the record's primary key: -->
結果をチャンク中にデータベース レコードを更新すると、チャンク結果が予期しない形で変化する可能性があります。チャンク中に取得したレコードを更新する予定がある場合は、代わりに `chunkById` メソッドを使用することが常に最善です。このメソッドは、レコードの主キーに基づいて結果を自動的にページ分割します。

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
`chunkById` メソッドと `lazyById` メソッドは、実行されるクエリに独自の「where」条件を追加するため、通常はクロージャ内で独自の条件を [logically group](#logical-grouping) する必要があります。

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
> チャンク コールバック内のレコードを更新または削除する場合、主キーまたは外部キーに変更を加えると、チャンク クエリに影響を与える可能性があります。これにより、チャンク化された結果にレコードが含まれない可能性があります。

<a name="streaming-results-lazily"></a>
<!-- ### Streaming Results Lazily -->
### Streaming Results Lazily

<!-- The `lazy` method works similarly to [the chunk method](#chunking-results) in the sense that it executes the query in chunks. However, instead of passing each chunk into a callback, the `lazy()` method returns a [LazyCollection](/docs/13.x/collections#lazy-collections), which lets you interact with the results as a single stream: -->
`lazy` メソッドは、クエリをチャンクで実行するという点で [the chunk method](#chunking-results) と同様に機能します。ただし、各チャンクをコールバックに渡す代わりに、`lazy()` メソッドは [LazyCollection](/docs/13.x/collections#lazy-collections) を返します。これにより、結果を単一のストリームとして操作できます。

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

<!-- Once again, if you plan to update the retrieved records while iterating over them, it is best to use the `lazyById` or `lazyByIdDesc` methods instead. These methods will automatically paginate the results based on the record's primary key: -->
繰り返しになりますが、取得したレコードを反復処理しながら更新する場合は、代わりに `lazyById` メソッドまたは `lazyByIdDesc` メソッドを使用することをお勧めします。これらのメソッドは、レコードの主キーに基づいて結果を自動的にページ分割します。

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> レコードを反復処理しながらレコードを更新または削除する場合、主キーまたは外部キーへの変更がチャンク クエリに影響を与える可能性があります。これにより、レコードが結果に含まれない可能性があります。

<a name="aggregates"></a>
<!-- ### Aggregates -->
### Aggregates

<!-- The query builder also provides a variety of methods for retrieving aggregate values like `count`, `max`, `min`, `avg`, and `sum`. You may call any of these methods after constructing your query: -->
クエリビルダは、`count`、`max`、`min`、`avg`、`sum` などの集計値を取得するためのさまざまなメソッドも提供します。クエリを作成した後、次のメソッドのいずれかを呼び出すことができます。

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

<!-- Of course, you may combine these methods with other clauses to fine-tune how your aggregate value is calculated: -->
もちろん、これらのメソッドを他の句と組み合わせて、集計値の計算方法を微調整することもできます。

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
<!-- #### Determining if Records Exist -->
#### Determining if Records Exist

<!-- Instead of using the `count` method to determine if any records exist that match your query's constraints, you may use the `exists` and `doesntExist` methods: -->
`count` メソッドを使用してクエリの制約に一致するレコードが存在するかどうかを確認する代わりに、`exists` メソッドと `doesntExist` メソッドを使用することもできます。

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
データベース テーブルからすべての列を選択する必要がない場合もあります。 `select` メソッドを使用すると、クエリにカスタムの「select」句を指定できます。

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

<!-- The `distinct` method allows you to force the query to return distinct results: -->
`distinct` メソッドを使用すると、クエリが個別の結果を返すように強制できます。

```php
$users = DB::table('users')->distinct()->get();
```

<!-- If you already have a query builder instance and you wish to add a column to its existing select clause, you may use the `addSelect` method: -->
クエリビルダ インスタンスがすでにあり、その既存の選択句に列を追加したい場合は、`addSelect` メソッドを使用できます。

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
<!-- ## Raw Expressions -->
## Raw Expressions

<!-- Sometimes you may need to insert an arbitrary string into a query. To create a raw string expression, you may use the `raw` method provided by the `DB` facade: -->
場合によっては、クエリに任意の文字列を挿入する必要があるかもしれません。生の文字列式を作成するには、`DB` ファサードによって提供される `raw` メソッドを使用できます。

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> 生のステートメントは文字列としてクエリに挿入されるため、SQL インジェクションの脆弱性が発生しないように細心の注意を払う必要があります。

<a name="raw-methods"></a>
<!-- ### Raw Methods -->
### Raw Methods

<!-- Instead of using the `DB::raw` method, you may also use the following methods to insert a raw expression into various parts of your query. **Remember, Laravel cannot guarantee that any query using raw expressions is protected against SQL injection vulnerabilities.** -->
`DB::raw` メソッドを使用する代わりに、次のメソッドを使用してクエリのさまざまな部分に生の式を挿入することもできます。 **Laravel では、生の式を使用したクエリが SQL インジェクションの脆弱性から保護されることを保証できないことに注意してください。**

<a name="selectraw"></a>
<!-- #### `selectRaw` -->
#### `selectRaw`

<!-- The `selectRaw` method can be used in place of `addSelect(DB::raw(/* ... *&#47;))`. This method accepts an optional array of bindings as its second argument: -->
`selectRaw` メソッドは、`addSelect(DB::raw(/* ... */))` の代わりに使用できます。このメソッドは、オプションのバインディングの配列を 2 番目の引数として受け入れます。

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
<!-- #### `whereRaw / orWhereRaw` -->
#### `whereRaw / orWhereRaw`

<!-- The `whereRaw` and `orWhereRaw` methods can be used to inject a raw "where" clause into your query. These methods accept an optional array of bindings as their second argument: -->
`whereRaw` メソッドと `orWhereRaw` メソッドを使用して、生の "where" 句をクエリに挿入できます。これらのメソッドは、オプションのバインディングの配列を 2 番目の引数として受け入れます。

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
<!-- #### `havingRaw / orHavingRaw` -->
#### `havingRaw / orHavingRaw`

<!-- The `havingRaw` and `orHavingRaw` methods may be used to provide a raw string as the value of the "having" clause. These methods accept an optional array of bindings as their second argument: -->
`havingRaw` メソッドと `orHavingRaw` メソッドを使用して、生の文字列を「having」句の値として提供できます。これらのメソッドは、オプションのバインディングの配列を 2 番目の引数として受け入れます。

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
`orderByRaw` メソッドを使用して、生の文字列を「order by」句の値として提供できます。

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
<!-- ### `groupByRaw` -->
### `groupByRaw`

<!-- The `groupByRaw` method may be used to provide a raw string as the value of the `group by` clause: -->
`groupByRaw` メソッドを使用して、生の文字列を `group by` 句の値として提供できます。

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
クエリビルダは、クエリに結合句を追加するために使用することもできます。基本的な「内部結合」を実行するには、クエリビルダ インスタンスで `join` メソッドを使用できます。 `join` メソッドに渡される最初の引数は結合する必要があるテーブルの名前で、残りの引数は結合の列制約を指定します。単一のクエリで複数のテーブルを結合することもできます。

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
「内部結合」の代わりに「左結合」または「右結合」を実行したい場合は、`leftJoin` メソッドまたは `rightJoin` メソッドを使用します。これらのメソッドは、`join` メソッドと同じシグネチャを持ちます。

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
`crossJoin` メソッドを使用して「クロス結合」を実行できます。クロス結合では、最初のテーブルと結合されたテーブルの間にデカルト積が生成されます。

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
<!-- #### Advanced Join Clauses -->
#### Advanced Join Clauses

<!-- You may also specify more advanced join clauses. To get started, pass a closure as the second argument to the `join` method. The closure will receive a `Illuminate\Database\Query\JoinClause` instance which allows you to specify constraints on the "join" clause: -->
より高度な結合句を指定することもできます。まず、2 番目の引数としてクロージャを `join` メソッドに渡します。クロージャは、「join」句に制約を指定できる `Illuminate\Database\Query\JoinClause` インスタンスを受け取ります。

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

<!-- If you would like to use a "where" clause on your joins, you may use the `where` and `orWhere` methods provided by the `JoinClause` instance. Instead of comparing two columns, these methods will compare the column against a value: -->
結合で「where」句を使用したい場合は、`JoinClause` インスタンスによって提供される `where` メソッドと `orWhere` メソッドを使用できます。これらのメソッドは、2 つの列を比較する代わりに、列を値と比較します。

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
`joinSub`、`leftJoinSub`、および `rightJoinSub` メソッドを使用して、クエリをサブクエリに結合できます。これらの各メソッドは、サブクエリ、そのテーブル エイリアス、および関連する列を定義するクロージャという 3 つの引数を受け取ります。この例では、ユーザーのコレクションを取得します。各ユーザー レコードには、ユーザーが最後に公開したブログ投稿の `created_at` タイムスタンプも含まれています。

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
> 横方向結合は現在、PostgreSQL、MySQL 8.0.14 以上、および SQL Server でサポートされています。

<!-- You may use the `joinLateral` and `leftJoinLateral` methods to perform a "lateral join" with a subquery. Each of these methods receives two arguments: the subquery and its table alias. The join condition(s) should be specified within the `where` clause of the given subquery. Lateral joins are evaluated for each row and can reference columns outside the subquery. -->
`joinLateral` メソッドと `leftJoinLateral` メソッドを使用して、サブクエリとの「横結合」を実行できます。これらの各メソッドは、サブクエリとそのテーブル エイリアスの 2 つの引数を受け取ります。結合条件は、指定されたサブクエリの `where` 句内で指定する必要があります。横方向結合は行ごとに評価され、サブクエリの外部の列を参照できます。

<!-- In this example, we will retrieve a collection of users as well as the user's three most recent blog posts. Each user can produce up to three rows in the result set: one for each of their most recent blog posts. The join condition is specified with a `whereColumn` clause within the subquery, referencing the current user row: -->
この例では、ユーザーのコレクションとユーザーの最新の 3 つのブログ投稿を取得します。各ユーザーは、結果セット内に最大 3 行 (最新のブログ投稿ごとに 1 行) を生成できます。結合条件は、サブクエリ内の `whereColumn` 句で指定され、現在のユーザー行を参照します。

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
クエリビルダは、2 つ以上のクエリを「結合」する便利な方法も提供します。たとえば、最初のクエリを作成し、`union` メソッドを使用して、それをさらに多くのクエリと結合できます。

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
`union` メソッドに加えて、クエリビルダは `unionAll` メソッドを提供します。 `unionAll` メソッドを使用して結合されたクエリでは、重複した結果は削除されません。 `unionAll` メソッドには、`union` メソッドと同じメソッド シグネチャがあります。

<a name="basic-where-clauses"></a>
<!-- ## Basic Where Clauses -->
## Basic Where Clauses

<a name="where-clauses"></a>
<!-- ### Where Clauses -->
### Where Clauses

<!-- You may use the query builder's `where` method to add "where" clauses to the query. The most basic call to the `where` method requires three arguments. The first argument is the name of the column. The second argument is an operator, which can be any of the database's supported operators. The third argument is the value to compare against the column's value. -->
クエリビルダの `where` メソッドを使用して、クエリに「where」句を追加できます。 `where` メソッドの最も基本的な呼び出しには 3 つの引数が必要です。最初の引数は列の名前です。 2 番目の引数は演算子で、データベースでサポートされている演算子のいずれかを使用できます。 3 番目の引数は、列の値と比較する値です。

<!-- For example, the following query retrieves users where the value of the `votes` column is equal to `100` and the value of the `age` column is greater than `35`: -->
たとえば、次のクエリは、`votes` 列の値が `100` に等しく、`age` 列の値が `35` より大きいユーザーを取得します。

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

<!-- For convenience, if you want to verify that a column is `=` to a given value, you may pass the value as the second argument to the `where` method. Laravel will assume you would like to use the `=` operator: -->
便宜上、列が特定の値に対して `=` であることを確認したい場合は、その値を 2 番目の引数として `where` メソッドに渡すことができます。 Laravel は、`=` 演算子を使用したいと想定します。

```php
$users = DB::table('users')->where('votes', 100)->get();
```

<!-- You may also provide an associative array to the `where` method to quickly query against multiple columns: -->
連想配列を `where` メソッドに指定して、複数の列に対してすばやくクエリを実行することもできます。

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

<!-- As previously mentioned, you may use any operator that is supported by your database system: -->
前述したように、データベース システムでサポートされている任意の演算子を使用できます。

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
条件の配列を `where` 関数に渡すこともできます。配列の各要素は、通常 `where` メソッドに渡される 3 つの引数を含む配列である必要があります。

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO は列名のバインドをサポートしていません。したがって、「order by」列を含め、クエリで参照される列名をユーザー入力によって決定することを決して許可しないでください。

> [!WARNING]
> MySQL と MariaDB は、文字列と数値の比較において、文字列を整数に自動的に型castします。このプロセスでは、数値以外の文字列が `0` に変換されるため、予期しない結果が生じる可能性があります。たとえば、テーブルに `aaa` の値を持つ `secret` 列があり、`User::where('secret', 0)` を実行すると、その行が返されます。これを回避するには、クエリで使用する前に、すべての値が適切な型に型castされていることを確認してください。

<a name="or-where-clauses"></a>
<!-- ### Or Where Clauses -->
### Or Where Clauses

<!-- When chaining together calls to the query builder's `where` method, the "where" clauses will be joined together using the `and` operator. However, you may use the `orWhere` method to join a clause to the query using the `or` operator. The `orWhere` method accepts the same arguments as the `where` method: -->
クエリビルダの `where` メソッドへの呼び出しを連鎖させる場合、「where」句は `and` 演算子を使用して結合されます。ただし、`orWhere` メソッドを使用して、`or` 演算子を使用して句をクエリに結合することもできます。 `orWhere` メソッドは、`where` メソッドと同じ引数を受け入れます。

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

<!-- If you need to group an "or" condition within parentheses, you may pass a closure as the first argument to the `orWhere` method: -->
「or」条件を括弧内でグループ化する必要がある場合は、最初の引数としてクロージャを `orWhere` メソッドに渡すことができます。

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
上記の例では、次の SQL が生成されます。

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> グローバル スコープが適用されるときの予期しない動作を避けるために、`orWhere` 呼び出しを常にグループ化する必要があります。

<a name="where-not-clauses"></a>
<!-- ### Where Not Clauses -->
### Where Not Clauses

<!-- The `whereNot` and `orWhereNot` methods may be used to negate a given group of query constraints. For example, the following query excludes products that are on clearance or which have a price that is less than ten: -->
`whereNot` メソッドと `orWhereNot` メソッドは、クエリ制約の特定のグループを無効にするために使用できます。たとえば、次のクエリでは、在庫処分中の製品や価格が 10 未満の製品が除外されます。

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
場合によっては、同じクエリ制約を複数の列に適用する必要がある場合があります。たとえば、指定されたリスト内の列が指定された値 `LIKE` であるすべてのレコードを取得したい場合があります。これは、`whereAny` メソッドを使用して実行できます。

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
上記のクエリの結果は次の SQL になります。

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
同様に、`whereAll` メソッドを使用して、指定されたすべての列が指定された制約に一致するレコードを取得できます。

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
上記のクエリの結果は次の SQL になります。

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

<!-- The `whereNone` method may be used to retrieve records where none of the given columns match a given constraint: -->
`whereNone` メソッドは、指定された列が指定された制約に一致しないレコードを取得するために使用できます。

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
上記のクエリの結果は次の SQL になります。

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
Laravel は、JSON 列タイプのサポートを提供するデータベースでの JSON 列タイプのクエリもサポートしています。現在、これには MariaDB 10.3 以降、MySQL 8.0 以降、PostgreSQL 12.0 以降、SQL Server 2017 以降、および SQLite 3.39.0 以降が含まれます。 JSON 列をクエリするには、`->` 演算子を使用します。

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

<!-- You may use the `whereJsonContains` and `whereJsonDoesntContain` methods to query JSON arrays: -->
`whereJsonContains` メソッドと `whereJsonDoesntContain` メソッドを使用して、JSON 配列をクエリできます。

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

<!-- If your application uses the MariaDB, MySQL, or PostgreSQL databases, you may pass an array of values to the `whereJsonContains` and `whereJsonDoesntContain` methods: -->
アプリケーションが MariaDB、MySQL、または PostgreSQL データベースを使用している場合は、値の配列を `whereJsonContains` および `whereJsonDoesntContain` メソッドに渡すことができます。

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

<!-- In addition, you may use the `whereJsonContainsKey` or `whereJsonDoesntContainKey` methods to retrieve the results that include or do not include a JSON key: -->
さらに、`whereJsonContainsKey` メソッドまたは `whereJsonDoesntContainKey` メソッドを使用して、JSON キーを含む、または含まない結果を取得することもできます。

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

<!-- Finally, you may use `whereJsonLength` method to query JSON arrays by their length: -->
最後に、`whereJsonLength` メソッドを使用して、JSON 配列を長さでクエリできます。

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
**どこのような場所 / またはどこのような場所 / どこのような場所ではない / またはどこのような場所ではない **

<!-- The `whereLike` method allows you to add "LIKE" clauses to your query for pattern matching. These methods provide a database-agnostic way of performing string matching queries, with the ability to toggle case-sensitivity. By default, string matching is case-insensitive: -->
`whereLike` メソッドを使用すると、パターン マッチングのためにクエリに「LIKE」句を追加できます。これらのメソッドは、大文字と小文字の区別を切り替える機能を備えた、データベースに依存しない文字列一致クエリの実行方法を提供します。デフォルトでは、文字列の照合では大文字と小文字が区別されません。

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

<!-- You can enable a case-sensitive search via the `caseSensitive` argument: -->
`caseSensitive` 引数を使用して、大文字と小文字を区別した検索を有効にできます。

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

<!-- The `orWhereLike` method allows you to add an "or" clause with a LIKE condition: -->
`orWhereLike` メソッドを使用すると、LIKE 条件を含む「or」句を追加できます。

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

<!-- The `whereNotLike` method allows you to add "NOT LIKE" clauses to your query: -->
`whereNotLike` メソッドを使用すると、クエリに「NOT LIKE」句を追加できます。

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

<!-- Similarly, you can use `orWhereNotLike` to add an "or" clause with a NOT LIKE condition: -->
同様に、`orWhereNotLike` を使用して、NOT LIKE 条件を含む「or」句を追加できます。

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike` 大文字と小文字を区別する検索オプションは、現在 SQL Server ではサポートされていません。

<!-- **whereIn / whereNotIn / orWhereIn / orWhereNotIn** -->
**どこで / どこでではない / またはどこでで / またはどこでではない **

<!-- The `whereIn` method verifies that a given column's value is contained within the given array: -->
`whereIn` メソッドは、指定された列の値が指定された配列内に含まれていることを検証します。

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

<!-- The `whereNotIn` method verifies that the given column's value is not contained in the given array: -->
`whereNotIn` メソッドは、指定された列の値が指定された配列に含まれていないことを検証します。

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

<!-- You may also provide a query object as the `whereIn` method's second argument: -->
`whereIn` メソッドの 2 番目の引数としてクエリ オブジェクトを指定することもできます。

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

<!-- The example above will produce the following SQL: -->
上記の例では、次の SQL が生成されます。

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 整数バインディングの大規模な配列をクエリに追加する場合、`whereIntegerInRaw` メソッドまたは `whereIntegerNotInRaw` メソッドを使用すると、メモリ使用量を大幅に削減できます。

<!-- **whereBetween / orWhereBetween** -->
**どこの間/またはどこの間**

<!-- The `whereBetween` method verifies that a column's value is between two values: -->
`whereBetween` メソッドは、列の値が 2 つの値の間にあることを検証します。

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

<!-- **whereNotBetween / orWhereNotBetween** -->
**whereNotBetween / または WhereNotBetween**

<!-- The `whereNotBetween` method verifies that a column's value lies outside of two values: -->
`whereNotBetween` メソッドは、列の値が次の 2 つの値の範囲外にあるかどうかを検証します。

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

<!-- **whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns** -->
**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

<!-- The `whereBetweenColumns` method verifies that a column's value is between the two values of two columns in the same table row: -->
`whereBetweenColumns` メソッドは、列の値が、同じテーブル行内の 2 つの列の 2 つの値の間にあることを検証します。

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

<!-- The `whereNotBetweenColumns` method verifies that a column's value lies outside the two values of two columns in the same table row: -->
`whereNotBetweenColumns` メソッドは、列の値が同じテーブル行内の 2 つの列の 2 つの値の外側にあることを検証します。

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

<!-- **whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween** -->
**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

<!-- The `whereValueBetween` method verifies that a given value is between the values of two columns of the same type in the same table row: -->
`whereValueBetween` メソッドは、指定された値が、同じテーブル行内の同じ型の 2 つの列の値の間にあることを検証します。

```php
$products = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

<!-- The `whereValueNotBetween` method verifies that a value lies outside the values of two columns in the same table row: -->
`whereValueNotBetween` メソッドは、値が同じテーブル行の 2 つの列の値の外側にあることを検証します。

```php
$products = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

<!-- **whereNull / whereNotNull / orWhereNull / orWhereNotNull** -->
**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

<!-- The `whereNull` method verifies that the value of the given column is `NULL`: -->
`whereNull` メソッドは、指定された列の値が `NULL` であることを検証します。

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

<!-- The `whereNotNull` method verifies that the column's value is not `NULL`: -->
`whereNotNull` メソッドは、列の値が `NULL` ではないことを検証します。

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

<!-- **whereNullSafeEquals / orWhereNullSafeEquals** -->
**whereNullSafeEquals / orWhereNullSafeEquals**

<!-- The `whereNullSafeEquals` and `orWhereNullSafeEquals` methods may be used to compare a column's value against a given value while treating two `NULL` values as equal: -->
`whereNullSafeEquals` と `orWhereNullSafeEquals` メソッドは、2つの `NULL` 値を等しいものとして扱いながら、列の値を指定した値と比較するために使用できます。

```php
$lastLoginIp = $request->input('last_login_ip');

$users = DB::table('users')
    ->whereNullSafeEquals('last_login_ip', $lastLoginIp)
    ->get();
```

<!-- **whereDate / whereMonth / whereDay / whereYear / whereTime** -->
**どこの日付 / どこの月 / どこの日 / どこの年 / どこの時間 **

<!-- The `whereDate` method may be used to compare a column's value against a date: -->
`whereDate` メソッドは、列の値を日付と比較するために使用できます。

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

<!-- The `whereMonth` method may be used to compare a column's value against a specific month: -->
`whereMonth` メソッドは、列の値を特定の月と比較するために使用できます。

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

<!-- The `whereDay` method may be used to compare a column's value against a specific day of the month: -->
`whereDay` メソッドは、列の値を月の特定の日と比較するために使用できます。

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

<!-- The `whereYear` method may be used to compare a column's value against a specific year: -->
`whereYear` メソッドは、列の値を特定の年と比較するために使用できます。

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

<!-- The `whereTime` method may be used to compare a column's value against a specific time: -->
`whereTime` メソッドは、列の値を特定の時間と比較するために使用できます。

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

<!-- **wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday** -->
**過去の場所 / 未来の場所 / 今日の場所 / 今日の場所 / 今日の場所 / 今日の場所 **

<!-- The `wherePast` and `whereFuture` methods may be used to determine if a column's value is in the past or future: -->
`wherePast` メソッドと `whereFuture` メソッドは、列の値が過去のものであるか未来のものであるかを判断するために使用できます。

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

<!-- The `whereNowOrPast` and `whereNowOrFuture` methods may be used to determine if a column's value is in the past or future, inclusive of the current date and time: -->
`whereNowOrPast` メソッドと `whereNowOrFuture` メソッドは、現在の日付と時刻を含め、列の値が過去のものであるか未来のものであるかを判断するために使用できます。

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

<!-- The `whereToday`, `whereBeforeToday`, and `whereAfterToday` methods may be used to determine if a column's value is today, before today, or after today, respectively: -->
`whereToday`、`whereBeforeToday`、および `whereAfterToday` メソッドは、それぞれ列の値が今日、今日より前、または今日以降であるかどうかを判断するために使用できます。

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
同様に、`whereTodayOrBefore` メソッドと `whereTodayOrAfter` メソッドを使用して、列の値が今日より前であるか今日以降であるかを判断できます (今日の日付も含みます)。

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

<!-- **whereColumn / orWhereColumn** -->
**whereColumn / orWhereColumn**

<!-- The `whereColumn` method may be used to verify that two columns are equal: -->
`whereColumn` メソッドを使用して、2 つの列が等しいことを確認できます。

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

<!-- You may also pass a comparison operator to the `whereColumn` method: -->
比較演算子を `whereColumn` メソッドに渡すこともできます。

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

<!-- You may also pass an array of column comparisons to the `whereColumn` method. These conditions will be joined using the `and` operator: -->
列比較の配列を `whereColumn` メソッドに渡すこともできます。これらの条件は、`and` 演算子を使用して結合されます。

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
場合によっては、クエリで目的の論理グループを作成するために、複数の "where" 句を括弧内でグループ化する必要がある場合があります。実際、予期しないクエリ動作を避けるために、通常は `orWhere` メソッドの呼び出しを常に括弧で囲んでグループ化する必要があります。これを実現するには、`where` メソッドにクロージャを渡すことができます。

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
ご覧のとおり、クロージャを `where` メソッドに渡すと、クエリビルダに制約グループを開始するように指示されます。クロージャはクエリビルダ インスタンスを受け取ります。これを使用して、括弧グループ内に含める制約を設定できます。上記の例では、次の SQL が生成されます。

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> グローバル スコープが適用されるときの予期しない動作を避けるために、`orWhere` 呼び出しを常にグループ化する必要があります。

<a name="advanced-where-clauses"></a>
<!-- ## Advanced Where Clauses -->
## Advanced Where Clauses

<a name="where-exists-clauses"></a>
<!-- ### Where Exists Clauses -->
### Where Exists Clauses

<!-- The `whereExists` method allows you to write "where exists" SQL clauses. The `whereExists` method accepts a closure which will receive a query builder instance, allowing you to define the query that should be placed inside of the "exists" clause: -->
`whereExists` メソッドを使用すると、「存在する場所」SQL 句を作成できます。 `whereExists` メソッドは、クエリビルダ インスタンスを受け取るクロージャを受け入れ、これにより、「exists」句内に配置する必要があるクエリを定義できます。

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
あるいは、クロージャの代わりにクエリ オブジェクトを `whereExists` メソッドに提供することもできます。

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

<!-- Both of the examples above will produce the following SQL: -->
上記の両方の例では、次の SQL が生成されます。

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
場合によっては、サブクエリの結果を指定された値と比較する「where」句を作成する必要があるかもしれません。これを行うには、クロージャと値を `where` メソッドに渡します。たとえば、次のクエリは、特定のタイプの最近の「メンバーシップ」を持つすべてのユーザーを取得します。

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
または、列をサブクエリの結果と比較する「where」句を作成する必要がある場合があります。これを行うには、列、演算子、およびクロージャを `where` メソッドに渡します。たとえば、次のクエリは、金額が平均より低いすべての収入レコードを取得します。

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
> フルテキストの where 句は現在、MariaDB、MySQL、PostgreSQL でサポートされています。

<!-- The `whereFullText` and `orWhereFullText` methods may be used to add full text "where" clauses to a query for columns that have [full text indexes](/docs/13.x/migrations#available-index-types). These methods will be transformed into the appropriate SQL for the underlying database system by Laravel. For example, a `MATCH AGAINST` clause will be generated for applications utilizing MariaDB or MySQL: -->
`whereFullText` メソッドと `orWhereFullText` メソッドは、[full text indexes](/docs/13.x/migrations#available-index-types) を持つ列のクエリにフルテキストの "where" 句を追加するために使用できます。これらのメソッドは、Laravel によって基礎となるデータベース システムに適した SQL に変換されます。たとえば、MariaDB または MySQL を利用するアプリケーションに対して `MATCH AGAINST` 句が生成されます。

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
<!-- ### Vector Similarity Clauses -->
### Vector Similarity Clauses

> [!NOTE]
> 現在、ベクトル類似性句は、`pgvector` 拡張機能を使用した PostgreSQL 接続でのみサポートされています。ベクトル列とインデックスの定義については、[migration documentation](/docs/13.x/migrations#available-column-types) を参照してください。

<!-- The `whereVectorSimilarTo` method filters results by cosine similarity to a given vector and orders the results by relevance. The `minSimilarity` threshold should be a value between `0.0` and `1.0`, where `1.0` is identical: -->
`whereVectorSimilarTo` メソッドは、指定されたベクトルに対するコサイン類似度によって結果をフィルター処理し、関連性によって結果を順序付けします。 `minSimilarity` しきい値は、`0.0` と `1.0` の間の値である必要があります。ここで、`1.0` は同一です。

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

<!-- When a plain string is given as the vector argument, Laravel will automatically generate embeddings for it using the [Laravel AI SDK](/docs/13.x/ai-sdk#embeddings): -->
プレーンな文字列がベクトル引数として指定されると、Laravel は [Laravel AI SDK](/docs/13.x/ai-sdk#embeddings) を使用してその文字列の埋め込みを自動的に生成します。

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

<!-- By default, `whereVectorSimilarTo` also orders results by distance (most similar first). You may disable this ordering by passing `false` as the `order` argument: -->
デフォルトでは、`whereVectorSimilarTo` は結果を距離によって並べ替えます (最も類似したものから順)。この順序付けを無効にするには、`false` を `order` 引数として渡します。

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

<!-- If you need more control, you may use the `selectVectorDistance`, `whereVectorDistanceLessThan`, and `orderByVectorDistance` methods independently: -->
より詳細な制御が必要な場合は、`selectVectorDistance`、`whereVectorDistanceLessThan`、および `orderByVectorDistance` メソッドを個別に使用できます。

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
PostgreSQL を利用する場合、`vector` 列を作成する前に、`pgvector` 拡張機能をロードする必要があります。

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
`orderBy` メソッドを使用すると、クエリの結果を特定の列で並べ替えることができます。 `orderBy` メソッドで受け入れられる最初の引数は並べ替えの基準となる列である必要があり、2 番目の引数は並べ替えの方向を決定し、`asc` または `desc` のいずれかになります。

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

<!-- To sort by multiple columns, you may simply invoke `orderBy` as many times as necessary: -->
複数の列で並べ替えるには、必要なだけ `orderBy` を呼び出すだけです。

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

<!-- The sort direction is optional, and is ascending by default. If you want to sort in descending order, you can specify the second parameter for the `orderBy` method, or just use `orderByDesc`: -->
並べ替え方向はオプションであり、デフォルトでは昇順です。降順で並べ替える場合は、`orderBy` メソッドの 2 番目のパラメーターを指定するか、単に `orderByDesc` を使用します。

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

<!-- Finally, using the `->` operator, the results can be sorted by a value within a JSON column: -->
最後に、`->` 演算子を使用して、結果を JSON 列内の値で並べ替えることができます。

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
`latest` メソッドと `oldest` メソッドを使用すると、結果を日付順に簡単に並べることができます。デフォルトでは、結果はテーブルの `created_at` 列によって並べられます。または、並べ替えの基準にする列名を渡すこともできます。

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
<!-- #### Random Ordering -->
#### Random Ordering

<!-- The `inRandomOrder` method may be used to sort the query results randomly. For example, you may use this method to fetch a random user: -->
`inRandomOrder` メソッドを使用して、クエリ結果をランダムに並べ替えることができます。たとえば、このメソッドを使用してランダムなユーザーを取得できます。

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
<!-- #### Removing Existing Orderings -->
#### Removing Existing Orderings

<!-- The `reorder` method removes all of the "order by" clauses that have previously been applied to the query: -->
`reorder` メソッドは、以前にクエリに適用されたすべての "order by" 句を削除します。

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

<!-- You may pass a column and direction when calling the `reorder` method in order to remove all existing "order by" clauses and apply an entirely new order to the query: -->
既存の「order by」句をすべて削除し、まったく新しい順序をクエリに適用するために、`reorder` メソッドを呼び出すときに列と方向を渡すことができます。

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<!-- For convenience, you may use the `reorderDesc` method to reorder the query results in descending order: -->
便宜上、`reorderDesc` メソッドを使用してクエリ結果を降順に並べ替えることができます。

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
ご想像のとおり、`groupBy` メソッドと `having` メソッドを使用してクエリ結果をグループ化できます。 `having` メソッドのシグネチャは、`where` メソッドのシグネチャと似ています。

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

<!-- You can use the `havingBetween` method to filter the results within a given range: -->
`havingBetween` メソッドを使用して、指定された範囲内の結果をフィルターできます。

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

<!-- You may pass multiple arguments to the `groupBy` method to group by multiple columns: -->
複数の引数を `groupBy` メソッドに渡して、複数の列でグループ化することができます。

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

<!-- To build more advanced `having` statements, see the [havingRaw](#raw-methods) method. -->
より高度な `having` ステートメントを作成するには、[havingRaw](#raw-methods) メソッドを参照してください。

<a name="limit-and-offset"></a>
<!-- ### Limit and Offset -->
### Limit and Offset

<!-- You may use the `limit` and `offset` methods to limit the number of results returned from the query or to skip a given number of results in the query: -->
`limit` メソッドと `offset` メソッドを使用して、クエリから返される結果の数を制限したり、クエリ内の指定された数の結果をスキップしたりできます。

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
場合によっては、特定のクエリ句を別の条件に基づいてクエリに適用したい場合があります。たとえば、受信 HTTP リクエストに特定の入力値が存在する場合にのみ、`where` ステートメントを適用することができます。これは、`when` メソッドを使用して実行できます。

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

<!-- The `when` method only executes the given closure when the first argument is `true`. If the first argument is `false`, the closure will not be executed. So, in the example above, the closure given to the `when` method will only be invoked if the `role` field is present on the incoming request and evaluates to `true`. -->
`when` メソッドは、最初の引数が `true` の場合にのみ、指定されたクロージャを実行します。最初の引数が `false` の場合、クロージャは実行されません。したがって、上記の例では、`when` メソッドに指定されたクロージャは、受信リクエストに `role` フィールドが存在し、`true` と評価される場合にのみ呼び出されます。

<!-- You may pass another closure as the third argument to the `when` method. This closure will only execute if the first argument evaluates as `false`. To illustrate how this feature may be used, we will use it to configure the default ordering of a query: -->
別のクロージャを `when` メソッドの 3 番目の引数として渡すことができます。このクロージャは、最初の引数が `false` として評価される場合にのみ実行されます。この機能がどのように使用されるかを説明するために、この機能を使用してクエリのデフォルトの順序を設定します。

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
クエリビルダは、データベース テーブルにレコードを挿入するために使用できる `insert` メソッドも提供します。 `insert` メソッドは、列名と値の配列を受け入れます。

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

<!-- You may insert several records at once by passing an array of arrays. Each array represents a record that should be inserted into the table: -->
配列の配列を渡すことで、複数のレコードを一度に挿入できます。各配列は、テーブルに挿入する必要があるレコードを表します。

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

<!-- The `insertOrIgnore` method will ignore errors while inserting records into the database. When using this method, you should be aware that duplicate record errors will be ignored and other types of errors may also be ignored depending on the database engine. For example, `insertOrIgnore` will [bypass MySQL's strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution): -->
`insertOrIgnore` メソッドは、データベースにレコードを挿入する際のエラーを無視します。この方法を使用する場合、重複レコード エラーは無視され、データベース エンジンによっては他の種類のエラーも無視される場合があることに注意してください。たとえば、`insertOrIgnore` は [bypass MySQL's strict mode](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution) になります。

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

<!-- The `insertUsing` method will insert new records into the table while using a subquery to determine the data that should be inserted: -->
`insertUsing` メソッドは、サブクエリを使用して挿入するデータを決定しながら、テーブルに新しいレコードを挿入します。

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
テーブルに自動インクリメント ID がある場合は、`insertGetId` メソッドを使用してレコードを挿入し、ID を取得します。

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL を使用する場合、`insertGetId` メソッドは、自動インクリメント列の名前が `id` であることを想定します。別の「シーケンス」から ID を取得したい場合は、列名を 2 番目のパラメーターとして `insertGetId` メソッドに渡すことができます。

<a name="upserts"></a>
<!-- ### Upserts -->
### Upserts

<!-- The `upsert` method will insert records that do not exist and update the records that already exist with new values that you may specify. The method's first argument consists of the values to insert or update, while the second argument lists the column(s) that uniquely identify records within the associated table. The method's third and final argument is an array of columns that should be updated if a matching record already exists in the database: -->
`upsert` メソッドは、存在しないレコードを挿入し、指定した新しい値で既存のレコードを更新します。メソッドの最初の引数は挿入または更新する値で構成され、2 番目の引数は関連するテーブル内のレコードを一意に識別する列をリストします。このメソッドの 3 番目と最後の引数は、一致するレコードがデータベースにすでに存在する場合に更新する必要がある列の配列です。

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
上の例では、Laravel は 2 つのレコードを挿入しようとします。同じ `departure` 列値と `destination` 列値を持つレコードがすでに存在する場合、Laravel はそのレコードの `price` 列を更新します。

> [!WARNING]
> SQL Server を除くすべてのデータベースでは、`upsert` メソッドの 2 番目の引数の列に「プライマリ」または「一意」インデックスが必要です。さらに、MariaDB および MySQL データベース ドライバは、`upsert` メソッドの 2 番目の引数を無視し、常にテーブルの「プライマリ」インデックスと「一意」インデックスを使用して既存のレコードを検出します。

<a name="update-statements"></a>
<!-- ## Update Statements -->
## Update Statements

<!-- In addition to inserting records into the database, the query builder can also update existing records using the `update` method. The `update` method, like the `insert` method, accepts an array of column and value pairs indicating the columns to be updated. The `update` method returns the number of affected rows. You may constrain the `update` query using `where` clauses: -->
クエリビルダは、データベースにレコードを挿入するだけでなく、`update` メソッドを使用して既存のレコードを更新することもできます。 `update` メソッドは、`insert` メソッドと同様に、更新される列を示す列と値のペアの配列を受け入れます。 `update` メソッドは、影響を受ける行の数を返します。 `where` 句を使用して、`update` クエリを制約できます。

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
<!-- #### Update or Insert -->
#### Update or Insert

<!-- Sometimes you may want to update an existing record in the database or create it if no matching record exists. In this scenario, the `updateOrInsert` method may be used. The `updateOrInsert` method accepts two arguments: an array of conditions by which to find the record, and an array of column and value pairs indicating the columns to be updated. -->
場合によっては、データベース内の既存のレコードを更新したり、一致するレコードが存在しない場合にレコードを作成したりすることが必要な場合があります。このシナリオでは、`updateOrInsert` メソッドが使用される可能性があります。 `updateOrInsert` メソッドは、レコードを検索するための条件の配列と、更新される列を示す列と値のペアの配列という 2 つの引数を受け入れます。

<!-- The `updateOrInsert` method will attempt to locate a matching database record using the first argument's column and value pairs. If the record exists, it will be updated with the values in the second argument. If the record cannot be found, a new record will be inserted with the merged attributes of both arguments: -->
`updateOrInsert` メソッドは、最初の引数の列と値のペアを使用して、一致するデータベース レコードの検索を試みます。レコードが存在する場合は、2 番目の引数の値で更新されます。レコードが見つからない場合は、両方の引数の属性を結合した新しいレコードが挿入されます。

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<!-- You may provide a closure to the `updateOrInsert` method to customize the attributes that are updated or inserted into the database based on the existence of a matching record: -->
`updateOrInsert` メソッドにクロージャーを提供して、一致するレコードの存在に基づいてデータベースに更新または挿入される属性をカスタマイズできます。

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
JSON 列を更新するときは、`->` 構文を使用して、JSON オブジェクト内の適切なキーを更新する必要があります。この操作は、MariaDB 10.3 以降、MySQL 5.7 以降、および PostgreSQL 9.5 以降でサポートされています。

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
<!-- ### Increment and Decrement -->
### Increment and Decrement

<!-- The query builder also provides convenient methods for incrementing or decrementing the value of a given column. Both of these methods accept at least one argument: the column to modify. A second argument may be provided to specify the amount by which the column should be incremented or decremented: -->
クエリビルダは、特定の列の値を増減する便利なメソッドも提供します。これらのメソッドは両方とも、少なくとも 1 つの引数、つまり変更する列を受け入れます。 2 番目の引数を指定して、列を増分または減分する量を指定できます。

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

<!-- If needed, you may also specify additional columns to update during the increment or decrement operation: -->
必要に応じて、インクリメントまたはデクリメント操作中に更新する追加の列を指定することもできます。

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

<!-- In addition, you may increment or decrement multiple columns at once using the `incrementEach` and `decrementEach` methods: -->
さらに、`incrementEach` および `decrementEach` メソッドを使用して、複数の列を一度に増加または減少させることができます。

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
クエリビルダの `delete` メソッドを使用して、テーブルからレコードを削除できます。 `delete` メソッドは、影響を受ける行の数を返します。 `delete` メソッドを呼び出す前に「where」句を追加することで、`delete` ステートメントを制約できます。

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
<!-- ## Pessimistic Locking -->
## Pessimistic Locking

<!-- The query builder also includes a few functions to help you achieve "pessimistic locking" when executing your `select` statements. To execute a statement with a "shared lock", you may call the `sharedLock` method. A shared lock prevents the selected rows from being modified until your transaction is committed: -->
クエリビルダには、`select` ステートメントの実行時に「悲観的ロック」を実現するのに役立つ関数もいくつか含まれています。 「共有ロック」を使用してステートメントを実行するには、`sharedLock` メソッドを呼び出すことができます。共有ロックにより、トランザクションがコミットされるまで、選択された行は変更されなくなります。

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

<!-- Alternatively, you may use the `lockForUpdate` method. A "for update" lock prevents the selected records from being modified or from being selected with another shared lock: -->
あるいは、`lockForUpdate` メソッドを使用することもできます。 「更新用」ロックは、選択されたレコードが変更されたり、別の共有ロックで選択されたりすることを防ぎます。

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

<!-- While not obligatory, it is recommended to wrap pessimistic locks within a [transaction](/docs/13.x/database#database-transactions). This ensures that the data retrieved remains unaltered in the database until the entire operation completes. In case of a failure, the transaction will roll back any changes and release the locks automatically: -->
必須ではありませんが、[transaction](/docs/13.x/database#database-transactions) 内で悲観的ロックをラップすることをお勧めします。これにより、操作全体が完了するまで、取得されたデータがデータベース内で変更されないことが保証されます。失敗した場合、トランザクションは変更をロールバックし、ロックを自動的に解放します。

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
アプリケーション全体でクエリ ロジックを繰り返している場合は、クエリビルダの `tap` メソッドと `pipe` メソッドを使用して、ロジックを再利用可能なオブジェクトに抽出できます。アプリケーションに次の 2 つの異なるクエリがあると想像してください。

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
クエリ間で共通する宛先フィルタリングを再利用可能なオブジェクトに抽出するとよいでしょう。

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
次に、クエリビルダの `tap` メソッドを使用して、オブジェクトのロジックをクエリに適用できます。

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
`tap` メソッドは常にクエリビルダを返します。クエリを実行して別の値を返すオブジェクトを抽出したい場合は、代わりに `pipe` メソッドを使用できます。

<!-- Consider the following query object that contains shared [pagination](/docs/13.x/pagination) logic used throughout an application. Unlike the `DestinationFilter`, which applies query conditions to the query, the `Paginate` object executes the query and returns a paginator instance: -->
アプリケーション全体で使用される共有 [pagination](/docs/13.x/pagination) ロジックを含む次のクエリ オブジェクトについて考えてみましょう。クエリ条件をクエリに適用する `DestinationFilter` とは異なり、`Paginate` オブジェクトはクエリを実行し、ページネータ インスタンスを返します。

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
クエリビルダの `pipe` メソッドを使用すると、このオブジェクトを利用して共有ページネーション ロジックを適用できます。

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
<!-- ## Debugging -->
## Debugging

<!-- You may use the `dd` and `dump` methods while building a query to dump the current query bindings and SQL. The `dd` method will display the debug information and then stop executing the request. The `dump` method will display the debug information but allow the request to continue executing: -->
クエリの構築中に `dd` メソッドと `dump` メソッドを使用して、現在のクエリ バインディングと SQL をダンプできます。 `dd` メソッドはデバッグ情報を表示し、リクエストの実行を停止します。 `dump` メソッドはデバッグ情報を表示しますが、リクエストの実行は継続できます。

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

<!-- The `dumpRawSql` and `ddRawSql` methods may be invoked on a query to dump the query's SQL with all parameter bindings properly substituted: -->
`dumpRawSql` メソッドと `ddRawSql` メソッドをクエリで呼び出して、すべてのパラメータ バインディングが適切に置換されたクエリの SQL をダンプできます。

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```

