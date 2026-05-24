# データベース: クエリビルダ (Database: Query Builder)

- [Introduction](#introduction)
- [データベースクエリの実行](#running-database-queries)
    - [チャンク化の結果](#chunking-results)
    - [結果を遅延的にストリーミングする](#streaming-results-lazily)
    - [Aggregates](#aggregates)
- [選択ステートメント](#select-statements)
- [生の式](#raw-expressions)
- [Joins](#joins)
- [Unions](#unions)
- [基本的な Where 句](#basic-where-clauses)
    - [Where句](#where-clauses)
    - [または Where 句](#or-where-clauses)
    - [Where Not句](#where-not-clauses)
    - [JSON Where句](#json-where-clauses)
    - [追加の Where 句](#additional-where-clauses)
    - [論理的なグループ化](#logical-grouping)
- [高度な Where 句](#advanced-where-clauses)
    - [Where Exists 条項](#where-exists-clauses)
    - [サブクエリの Where 句](#subquery-where-clauses)
    - [全文 Where 句](#full-text-where-clauses)
- [順序付け、グループ化、制限およびオフセット](#ordering-grouping-limit-and-offset)
    - [Ordering](#ordering)
    - [Grouping](#grouping)
    - [リミットとオフセット](#limit-and-offset)
- [条件節](#conditional-clauses)
- [ステートメントの挿入](#insert-statements)
    - [Upserts](#upserts)
- [更新ステートメント](#update-statements)
    - [JSON列の更新](#updating-json-columns)
    - [インクリメントとデクリメント](#increment-and-decrement)
- [ステートメントの削除](#delete-statements)
- [悲観的ロック](#pessimistic-locking)
- [Debugging](#debugging)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel のデータベース クエリビルダは、データベース クエリを作成および実行するための便利で流暢なインターフェイスを提供します。これはアプリケーションでほとんどのデータベース操作を実行するために使用でき、Laravel でサポートされているすべてのデータベース システムと完全に連携します。

Laravel クエリビルダは、PDO パラメーター バインディングを使用して、アプリケーションを SQL インジェクション攻撃から保護します。クエリ バインディングとしてクエリビルダに渡される文字列をクリーンアップまたはサニタイズする必要はありません。

> **警告**
> PDO は列名のバインドをサポートしていません。したがって、「order by」列を含め、クエリで参照される列名をユーザー入力によって決定することを決して許可しないでください。

<a name="running-database-queries"></a>
## データベースクエリの実行 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### テーブルからすべての行を取得する

`DB` ファサードによって提供される `table` メソッドを使用して、クエリを開始できます。 `table` メソッドは、指定されたテーブルの流暢なクエリビルダ インスタンスを返します。これにより、クエリにさらに多くの制約を連鎖させ、最後に `get` メソッドを使用してクエリの結果を取得できます。

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

`get` メソッドは、クエリの結果を含む `Illuminate\Support\Collection` インスタンスを返します。各結果は PHP `stdClass` オブジェクトのインスタンスです。オブジェクトのプロパティとして列にアクセスすることで、各列の値にアクセスできます。

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')->get();

    foreach ($users as $user) {
        echo $user->name;
    }

> **注記**
> Laravel コレクションは、データのマッピングと削減のための非常に強力なさまざまな方法を提供します。 Laravel コレクションの詳細については、[コレクションのドキュメント](/docs/{{version}}/collections) をチェックしてください。

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### テーブルから単一の行/列を取得する

データベース テーブルから 1 つの行を取得するだけの場合は、`DB` ファサードの `first` メソッドを使用できます。このメソッドは、単一の `stdClass` オブジェクトを返します。

    $user = DB::table('users')->where('name', 'John')->first();

    return $user->email;

行全体が必要ない場合は、`value` メソッドを使用してレコードから単一の値を抽出できます。このメソッドは列の値を直接返します。

    $email = DB::table('users')->where('name', 'John')->value('email');

`id` 列の値によって単一行を取得するには、`find` メソッドを使用します。

    $user = DB::table('users')->find(3);

<a name="retrieving-a-list-of-column-values"></a>
#### 列値のリストの取得

単一列の値を含む `Illuminate\Support\Collection` インスタンスを取得したい場合は、`pluck` メソッドを使用できます。この例では、ユーザーのタイトルのコレクションを取得します。

    use Illuminate\Support\Facades\DB;

    $titles = DB::table('users')->pluck('title');

    foreach ($titles as $title) {
        echo $title;
    }

`pluck` メソッドに 2 番目の引数を指定することで、結果のコレクションがキーとして使用する列を指定できます。

    $titles = DB::table('users')->pluck('title', 'name');

    foreach ($titles as $name => $title) {
        echo $title;
    }

<a name="chunking-results"></a>
### チャンク化の結果

数千のデータベース レコードを操作する必要がある場合は、`DB` ファサードによって提供される `chunk` メソッドの使用を検討してください。このメソッドは、一度に結果の小さなチャンクを取得し、各チャンクを処理のためにクロージャにフィードします。たとえば、`users` テーブル全体を一度に 100 レコードずつ取得してみましょう。

    use Illuminate\Support\Facades\DB;

    DB::table('users')->orderBy('id')->chunk(100, function ($users) {
        foreach ($users as $user) {
            //
        }
    });

クロージャから `false` を返すことで、それ以上のチャンクの処理を停止できます。

    DB::table('users')->orderBy('id')->chunk(100, function ($users) {
        // Process the records...

        return false;
    });

結果をチャンク中にデータベース レコードを更新すると、チャンク結果が予期しない形で変化する可能性があります。チャンク中に取得したレコードを更新する予定がある場合は、代わりに `chunkById` メソッドを使用することが常に最善です。このメソッドは、レコードの主キーに基づいて結果を自動的にページ分割します。

    DB::table('users')->where('active', false)
        ->chunkById(100, function ($users) {
            foreach ($users as $user) {
                DB::table('users')
                    ->where('id', $user->id)
                    ->update(['active' => true]);
            }
        });

> **警告**
> チャンク コールバック内のレコードを更新または削除する場合、主キーまたは外部キーに変更を加えると、チャンク クエリに影響を与える可能性があります。これにより、チャンク化された結果にレコードが含まれない可能性があります。

<a name="streaming-results-lazily"></a>
### 結果を遅延的にストリーミングする

`lazy` メソッドは、クエリをチャンクで実行するという点で [`chunk` メソッド](#chunking-results) と同様に機能します。ただし、各チャンクをコールバックに渡す代わりに、`lazy()` メソッドは [`LazyCollection`](/docs/{{version}}/collections#lazy-collections) を返します。これにより、結果を単一のストリームとして操作できます。

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function ($user) {
    //
});
```

繰り返しになりますが、取得したレコードを反復処理しながら更新する場合は、代わりに `lazyById` メソッドまたは `lazyByIdDesc` メソッドを使用することをお勧めします。これらのメソッドは、レコードの主キーに基づいて結果を自動的にページ分割します。

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function ($user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> **警告**
> レコードを反復処理しながらレコードを更新または削除する場合、主キーまたは外部キーへの変更がチャンク クエリに影響を与える可能性があります。これにより、レコードが結果に含まれない可能性があります。

<a name="aggregates"></a>
### 集合体

クエリビルダは、`count`、`max`、`min`、`avg`、`sum` などの集計値を取得するためのさまざまなメソッドも提供します。クエリを作成した後、次のメソッドのいずれかを呼び出すことができます。

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')->count();

    $price = DB::table('orders')->max('price');

もちろん、これらのメソッドを他の句と組み合わせて、集計値の計算方法を微調整することもできます。

    $price = DB::table('orders')
                    ->where('finalized', 1)
                    ->avg('price');

<a name="determining-if-records-exist"></a>
#### レコードが存在するかどうかの確認

`count` メソッドを使用してクエリの制約に一致するレコードが存在するかどうかを確認する代わりに、`exists` メソッドと `doesntExist` メソッドを使用することもできます。

    if (DB::table('orders')->where('finalized', 1)->exists()) {
        // ...
    }

    if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
        // ...
    }

<a name="select-statements"></a>
## 選択ステートメント (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 句の指定

データベース テーブルからすべての列を選択する必要がない場合もあります。 `select` メソッドを使用すると、クエリにカスタムの「select」句を指定できます。

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')
                ->select('name', 'email as user_email')
                ->get();

`distinct` メソッドを使用すると、クエリが個別の結果を返すように強制できます。

    $users = DB::table('users')->distinct()->get();

クエリビルダ インスタンスがすでにあり、その既存の選択句に列を追加したい場合は、`addSelect` メソッドを使用できます。

    $query = DB::table('users')->select('name');

    $users = $query->addSelect('age')->get();

<a name="raw-expressions"></a>
## 生の式 (Raw Expressions)

場合によっては、クエリに任意の文字列を挿入する必要があるかもしれません。生の文字列式を作成するには、`DB` ファサードによって提供される `raw` メソッドを使用できます。

    $users = DB::table('users')
                 ->select(DB::raw('count(*) as user_count, status'))
                 ->where('status', '<>', 1)
                 ->groupBy('status')
                 ->get();

> **警告**
> 生のステートメントは文字列としてクエリに挿入されるため、SQL インジェクションの脆弱性が発生しないように細心の注意を払う必要があります。

<a name="raw-methods"></a>
### 生のメソッド

`DB::raw` メソッドを使用する代わりに、次のメソッドを使用してクエリのさまざまな部分に生の式を挿入することもできます。 **Laravel では、生の式を使用したクエリが SQL インジェクションの脆弱性から保護されていることを保証できないことに注意してください。**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` メソッドは、`addSelect(DB::raw(/* ... */))` の代わりに使用できます。このメソッドは、オプションのバインディングの配列を 2 番目の引数として受け入れます。

    $orders = DB::table('orders')
                    ->selectRaw('price * ? as price_with_tax', [1.0825])
                    ->get();

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` メソッドと `orWhereRaw` メソッドを使用して、生の "where" 句をクエリに挿入できます。これらのメソッドは、オプションのバインディングの配列を 2 番目の引数として受け入れます。

    $orders = DB::table('orders')
                    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                    ->get();

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` メソッドと `orHavingRaw` メソッドを使用して、生の文字列を「having」句の値として提供できます。これらのメソッドは、オプションのバインディングの配列を 2 番目の引数として受け入れます。

    $orders = DB::table('orders')
                    ->select('department', DB::raw('SUM(price) as total_sales'))
                    ->groupBy('department')
                    ->havingRaw('SUM(price) > ?', [2500])
                    ->get();

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` メソッドを使用して、生の文字列を「order by」句の値として提供できます。

    $orders = DB::table('orders')
                    ->orderByRaw('updated_at - created_at DESC')
                    ->get();

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` メソッドを使用して、生の文字列を `group by` 句の値として提供できます。

    $orders = DB::table('orders')
                    ->select('city', 'state')
                    ->groupByRaw('city, state')
                    ->get();

<a name="joins"></a>
## 結合します (Joins)

<a name="inner-join-clause"></a>
#### 内部結合句

クエリビルダは、クエリに結合句を追加するために使用することもできます。基本的な「内部結合」を実行するには、クエリビルダ インスタンスで `join` メソッドを使用できます。 `join` メソッドに渡される最初の引数は結合する必要があるテーブルの名前で、残りの引数は結合の列制約を指定します。単一のクエリで複数のテーブルを結合することもできます。

    use Illuminate\Support\Facades\DB;

    $users = DB::table('users')
                ->join('contacts', 'users.id', '=', 'contacts.user_id')
                ->join('orders', 'users.id', '=', 'orders.user_id')
                ->select('users.*', 'contacts.phone', 'orders.price')
                ->get();

<a name="left-join-right-join-clause"></a>
#### 左結合/右結合節

「内部結合」の代わりに「左結合」または「右結合」を実行したい場合は、`leftJoin` メソッドまたは `rightJoin` メソッドを使用します。これらのメソッドは、`join` メソッドと同じシグネチャを持ちます。

    $users = DB::table('users')
                ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

    $users = DB::table('users')
                ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
                ->get();

<a name="cross-join-clause"></a>
#### 相互結合節

`crossJoin` メソッドを使用して「クロス結合」を実行できます。クロス結合では、最初のテーブルと結合されたテーブルの間にデカルト積が生成されます。

    $sizes = DB::table('sizes')
                ->crossJoin('colors')
                ->get();

<a name="advanced-join-clauses"></a>
#### 高度な結合句

より高度な結合句を指定することもできます。まず、2 番目の引数としてクロージャを `join` メソッドに渡します。クロージャは、「join」句に制約を指定できる `Illuminate\Database\Query\JoinClause` インスタンスを受け取ります。

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
            })
            ->get();

結合で「where」句を使用したい場合は、`JoinClause` インスタンスによって提供される `where` メソッドと `orWhere` メソッドを使用できます。これらのメソッドは、2 つの列を比較する代わりに、列を値と比較します。

    DB::table('users')
            ->join('contacts', function ($join) {
                $join->on('users.id', '=', 'contacts.user_id')
                     ->where('contacts.user_id', '>', 5);
            })
            ->get();

<a name="subquery-joins"></a>
#### サブクエリ結合

`joinSub`、`leftJoinSub`、および `rightJoinSub` メソッドを使用して、クエリをサブクエリに結合できます。これらの各メソッドは、サブクエリ、そのテーブル エイリアス、および関連する列を定義するクロージャという 3 つの引数を受け取ります。この例では、ユーザーのコレクションを取得します。各ユーザー レコードには、ユーザーが最後に公開したブログ投稿の `created_at` タイムスタンプも含まれています。

    $latestPosts = DB::table('posts')
                       ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
                       ->where('is_published', true)
                       ->groupBy('user_id');

    $users = DB::table('users')
            ->joinSub($latestPosts, 'latest_posts', function ($join) {
                $join->on('users.id', '=', 'latest_posts.user_id');
            })->get();

<a name="unions"></a>
## 労働組合 (Unions)

クエリビルダは、2 つ以上のクエリを「結合」する便利な方法も提供します。たとえば、最初のクエリを作成し、`union` メソッドを使用して、それをさらに多くのクエリと結合できます。

    use Illuminate\Support\Facades\DB;

    $first = DB::table('users')
                ->whereNull('first_name');

    $users = DB::table('users')
                ->whereNull('last_name')
                ->union($first)
                ->get();

`union` メソッドに加えて、クエリビルダは `unionAll` メソッドを提供します。 `unionAll` メソッドを使用して結合されたクエリでは、重複した結果は削除されません。 `unionAll` メソッドには、`union` メソッドと同じメソッド シグネチャがあります。

<a name="basic-where-clauses"></a>
## 基本的な Where 句 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where句

クエリビルダの `where` メソッドを使用して、クエリに「where」句を追加できます。 `where` メソッドの最も基本的な呼び出しには 3 つの引数が必要です。最初の引数は列の名前です。 2 番目の引数は演算子で、データベースでサポートされている演算子のいずれかを使用できます。 3 番目の引数は、列の値と比較する値です。

たとえば、次のクエリは、`votes` 列の値が `100` に等しく、`age` 列の値が `35` より大きいユーザーを取得します。

    $users = DB::table('users')
                    ->where('votes', '=', 100)
                    ->where('age', '>', 35)
                    ->get();

便宜上、列が特定の値に対して `=` であることを確認したい場合は、その値を 2 番目の引数として `where` メソッドに渡すことができます。 Laravel は、`=` 演算子を使用したいと想定します。

    $users = DB::table('users')->where('votes', 100)->get();

前述したように、データベース システムでサポートされている任意の演算子を使用できます。

    $users = DB::table('users')
                    ->where('votes', '>=', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('votes', '<>', 100)
                    ->get();

    $users = DB::table('users')
                    ->where('name', 'like', 'T%')
                    ->get();

条件の配列を `where` 関数に渡すこともできます。配列の各要素は、通常 `where` メソッドに渡される 3 つの引数を含む配列である必要があります。

    $users = DB::table('users')->where([
        ['status', '=', '1'],
        ['subscribed', '<>', '1'],
    ])->get();

> **警告**
> PDO は列名のバインドをサポートしていません。したがって、「order by」列を含め、クエリで参照される列名をユーザー入力によって決定することを決して許可しないでください。

<a name="or-where-clauses"></a>
### または Where 句

クエリビルダの `where` メソッドへの呼び出しを連鎖させる場合、「where」句は `and` 演算子を使用して結合されます。ただし、`orWhere` メソッドを使用して、`or` 演算子を使用して句をクエリに結合することもできます。 `orWhere` メソッドは、`where` メソッドと同じ引数を受け入れます。

    $users = DB::table('users')
                        ->where('votes', '>', 100)
                        ->orWhere('name', 'John')
                        ->get();

「or」条件を括弧内でグループ化する必要がある場合は、最初の引数としてクロージャを `orWhere` メソッドに渡すことができます。

    $users = DB::table('users')
                ->where('votes', '>', 100)
                ->orWhere(function($query) {
                    $query->where('name', 'Abigail')
                          ->where('votes', '>', 50);
                })
                ->get();

上記の例では、次の SQL が生成されます。

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> **警告**
> グローバル スコープが適用されるときの予期しない動作を避けるために、`orWhere` 呼び出しを常にグループ化する必要があります。

<a name="where-not-clauses"></a>
### Where Not句

`whereNot` メソッドと `orWhereNot` メソッドは、クエリ制約の特定のグループを無効にするために使用できます。たとえば、次のクエリでは、在庫処分中の製品や価格が 10 未満の製品が除外されます。

    $products = DB::table('products')
                    ->whereNot(function ($query) {
                        $query->where('clearance', true)
                              ->orWhere('price', '<', 10);
                    })
                    ->get();

<a name="json-where-clauses"></a>
### JSON Where句

Laravel は、JSON 列タイプのサポートを提供するデータベースでの JSON 列タイプのクエリもサポートしています。現在、これには MySQL 5.7 以降、PostgreSQL、SQL Server 2016、および SQLite 3.39.0 ([JSON1拡張子](https://www.sqlite.org/json1.html) を含む) が含まれます。 JSON 列をクエリするには、`->` 演算子を使用します。

    $users = DB::table('users')
                    ->where('preferences->dining->meal', 'salad')
                    ->get();

`whereJsonContains` を使用して JSON 配列をクエリできます。この機能は、SQLite データベース バージョン 3.38.0 より前のバージョンではサポートされていません。

    $users = DB::table('users')
                    ->whereJsonContains('options->languages', 'en')
                    ->get();

アプリケーションが MySQL または PostgreSQL データベースを使用している場合は、値の配列を `whereJsonContains` メソッドに渡すことができます。

    $users = DB::table('users')
                    ->whereJsonContains('options->languages', ['en', 'de'])
                    ->get();

`whereJsonLength` メソッドを使用して、JSON 配列を長さでクエリできます。

    $users = DB::table('users')
                    ->whereJsonLength('options->languages', 0)
                    ->get();

    $users = DB::table('users')
                    ->whereJsonLength('options->languages', '>', 1)
                    ->get();

<a name="additional-where-clauses"></a>
### 追加の Where 句

**どこの間/またはどこの間**

`whereBetween` メソッドは、列の値が 2 つの値の間にあることを検証します。

    $users = DB::table('users')
               ->whereBetween('votes', [1, 100])
               ->get();

**whereNotBetween / または WhereNotBetween**

`whereNotBetween` メソッドは、列の値が次の 2 つの値の範囲外にあるかどうかを検証します。

    $users = DB::table('users')
                        ->whereNotBetween('votes', [1, 100])
                        ->get();

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` メソッドは、列の値が、同じテーブル行内の 2 つの列の 2 つの値の間にあることを検証します。

    $patients = DB::table('patients')
                           ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                           ->get();

`whereNotBetweenColumns` メソッドは、列の値が同じテーブル行内の 2 つの列の 2 つの値の外側にあることを検証します。

    $patients = DB::table('patients')
                           ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                           ->get();

**どこで / どこでではない / またはどこでで / またはどこでではない **

`whereIn` メソッドは、指定された列の値が指定された配列内に含まれていることを検証します。

    $users = DB::table('users')
                        ->whereIn('id', [1, 2, 3])
                        ->get();

`whereNotIn` メソッドは、指定された列の値が指定された配列に含まれていないことを検証します。

    $users = DB::table('users')
                        ->whereNotIn('id', [1, 2, 3])
                        ->get();

`whereIn` メソッドの 2 番目の引数としてクエリ オブジェクトを指定することもできます。

    $activeUsers = DB::table('users')->select('id')->where('is_active', 1);

    $users = DB::table('comments')
                        ->whereIn('user_id', $activeUsers)
                        ->get();

上記の例では、次の SQL が生成されます。

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> **警告**
> 整数バインディングの大規模な配列をクエリに追加する場合、`whereIntegerInRaw` メソッドまたは `whereIntegerNotInRaw` メソッドを使用すると、メモリ使用量を大幅に削減できます。

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` メソッドは、指定された列の値が `NULL` であることを検証します。

    $users = DB::table('users')
                    ->whereNull('updated_at')
                    ->get();

`whereNotNull` メソッドは、列の値が `NULL` ではないことを検証します。

    $users = DB::table('users')
                    ->whereNotNull('updated_at')
                    ->get();

**どこの日付 / どこの月 / どこの日 / どこの年 / どこの時間 **

`whereDate` メソッドは、列の値を日付と比較するために使用できます。

    $users = DB::table('users')
                    ->whereDate('created_at', '2016-12-31')
                    ->get();

`whereMonth` メソッドは、列の値を特定の月と比較するために使用できます。

    $users = DB::table('users')
                    ->whereMonth('created_at', '12')
                    ->get();

`whereDay` メソッドは、列の値を月の特定の日と比較するために使用できます。

    $users = DB::table('users')
                    ->whereDay('created_at', '31')
                    ->get();

`whereYear` メソッドは、列の値を特定の年と比較するために使用できます。

    $users = DB::table('users')
                    ->whereYear('created_at', '2016')
                    ->get();

`whereTime` メソッドは、列の値を特定の時間と比較するために使用できます。

    $users = DB::table('users')
                    ->whereTime('created_at', '=', '11:20:45')
                    ->get();

**whereColumn / orWhereColumn**

`whereColumn` メソッドを使用して、2 つの列が等しいことを確認できます。

    $users = DB::table('users')
                    ->whereColumn('first_name', 'last_name')
                    ->get();

比較演算子を `whereColumn` メソッドに渡すこともできます。

    $users = DB::table('users')
                    ->whereColumn('updated_at', '>', 'created_at')
                    ->get();

列比較の配列を `whereColumn` メソッドに渡すこともできます。これらの条件は、`and` 演算子を使用して結合されます。

    $users = DB::table('users')
                    ->whereColumn([
                        ['first_name', '=', 'last_name'],
                        ['updated_at', '>', 'created_at'],
                    ])->get();

<a name="logical-grouping"></a>
### 論理的なグループ化

場合によっては、クエリで目的の論理グループを作成するために、複数の "where" 句を括弧内でグループ化する必要がある場合があります。実際、予期しないクエリ動作を避けるために、通常は `orWhere` メソッドの呼び出しを常に括弧で囲んでグループ化する必要があります。これを実現するには、`where` メソッドにクロージャを渡すことができます。

    $users = DB::table('users')
               ->where('name', '=', 'John')
               ->where(function ($query) {
                   $query->where('votes', '>', 100)
                         ->orWhere('title', '=', 'Admin');
               })
               ->get();

ご覧のとおり、クロージャを `where` メソッドに渡すと、クエリビルダに制約グループを開始するように指示されます。クロージャはクエリビルダ インスタンスを受け取ります。これを使用して、括弧グループ内に含める制約を設定できます。上記の例では、次の SQL が生成されます。

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> **警告**
> グローバル スコープが適用されるときの予期しない動作を避けるために、`orWhere` 呼び出しを常にグループ化する必要があります。

<a name="advanced-where-clauses"></a>
### 高度な Where 句

<a name="where-exists-clauses"></a>
### Where Exists 条項

`whereExists` メソッドを使用すると、「存在する場所」SQL 句を作成できます。 `whereExists` メソッドは、クエリビルダ インスタンスを受け取るクロージャを受け入れ、これにより、「exists」句内に配置する必要があるクエリを定義できます。

    $users = DB::table('users')
               ->whereExists(function ($query) {
                   $query->select(DB::raw(1))
                         ->from('orders')
                         ->whereColumn('orders.user_id', 'users.id');
               })
               ->get();

上記のクエリは次の SQL を生成します。

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### サブクエリの Where 句

場合によっては、サブクエリの結果を指定された値と比較する「where」句を作成する必要があるかもしれません。これを行うには、クロージャと値を `where` メソッドに渡します。たとえば、次のクエリは、特定のタイプの最近の「メンバーシップ」を持つすべてのユーザーを取得します。

    use App\Models\User;

    $users = User::where(function ($query) {
        $query->select('type')
            ->from('membership')
            ->whereColumn('membership.user_id', 'users.id')
            ->orderByDesc('membership.start_date')
            ->limit(1);
    }, 'Pro')->get();

または、列をサブクエリの結果と比較する「where」句を作成する必要がある場合があります。これを行うには、列、演算子、およびクロージャを `where` メソッドに渡します。たとえば、次のクエリは、金額が平均より低いすべての収入レコードを取得します。

    use App\Models\Income;

    $incomes = Income::where('amount', '<', function ($query) {
        $query->selectRaw('avg(i.amount)')->from('incomes as i');
    })->get();

<a name="full-text-where-clauses"></a>
### 全文 Where 句

> **警告**
> フルテキストの where 句は現在、MySQL と PostgreSQL でサポートされています。

`whereFullText` メソッドと `orWhereFullText` メソッドは、[全文インデックス](/docs/{{version}}/migrations#available-index-types) を持つ列のクエリにフルテキストの "where" 句を追加するために使用できます。これらのメソッドは、Laravel によって基礎となるデータベース システムに適した SQL に変換されます。たとえば、MySQL を利用するアプリケーションに対して `MATCH AGAINST` 句が生成されます。

    $users = DB::table('users')
               ->whereFullText('bio', 'web developer')
               ->get();

<a name="ordering-grouping-limit-and-offset"></a>
## 順序付け、グループ化、制限およびオフセット (Ordering, Grouping, Limit & Offset)

<a name="ordering"></a>
### 注文

<a name="orderby"></a>
#### `orderBy` メソッド

`orderBy` メソッドを使用すると、クエリの結果を特定の列で並べ替えることができます。 `orderBy` メソッドで受け入れられる最初の引数は並べ替えの基準となる列である必要があり、2 番目の引数は並べ替えの方向を決定し、`asc` または `desc` のいずれかになります。

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->get();

複数の列で並べ替えるには、必要なだけ `orderBy` を呼び出すだけです。

    $users = DB::table('users')
                    ->orderBy('name', 'desc')
                    ->orderBy('email', 'asc')
                    ->get();

<a name="latest-oldest"></a>
#### `latest` メソッドと `oldest` メソッド

`latest` メソッドと `oldest` メソッドを使用すると、結果を日付順に簡単に並べることができます。デフォルトでは、結果はテーブルの `created_at` 列によって並べられます。または、並べ替えの基準にする列名を渡すこともできます。

    $user = DB::table('users')
                    ->latest()
                    ->first();

<a name="random-ordering"></a>
#### ランダムな順序付け

`inRandomOrder` メソッドを使用して、クエリ結果をランダムに並べ替えることができます。たとえば、このメソッドを使用してランダムなユーザーを取得できます。

    $randomUser = DB::table('users')
                    ->inRandomOrder()
                    ->first();

<a name="removing-existing-orderings"></a>
#### 既存の注文の削除

`reorder` メソッドは、以前にクエリに適用されたすべての "order by" 句を削除します。

    $query = DB::table('users')->orderBy('name');

    $unorderedUsers = $query->reorder()->get();

既存の「order by」句をすべて削除し、まったく新しい順序をクエリに適用するために、`reorder` メソッドを呼び出すときに列と方向を渡すことができます。

    $query = DB::table('users')->orderBy('name');

    $usersOrderedByEmail = $query->reorder('email', 'desc')->get();

<a name="grouping"></a>
### グループ化

<a name="groupby-having"></a>
#### `groupBy` メソッドと `having` メソッド

ご想像のとおり、`groupBy` メソッドと `having` メソッドを使用してクエリ結果をグループ化できます。 `having` メソッドのシグネチャは、`where` メソッドのシグネチャと似ています。

    $users = DB::table('users')
                    ->groupBy('account_id')
                    ->having('account_id', '>', 100)
                    ->get();

`havingBetween` メソッドを使用して、指定された範囲内の結果をフィルターできます。

    $report = DB::table('orders')
                    ->selectRaw('count(id) as number_of_orders, customer_id')
                    ->groupBy('customer_id')
                    ->havingBetween('number_of_orders', [5, 15])
                    ->get();

複数の引数を `groupBy` メソッドに渡して、複数の列でグループ化することができます。

    $users = DB::table('users')
                    ->groupBy('first_name', 'status')
                    ->having('account_id', '>', 100)
                    ->get();

より高度な `having` ステートメントを作成するには、[`havingRaw`](#raw-methods) メソッドを参照してください。

<a name="limit-and-offset"></a>
### リミットとオフセット

<a name="skip-take"></a>
#### `skip` メソッドと `take` メソッド

`skip` メソッドと `take` メソッドを使用して、クエリから返される結果の数を制限したり、クエリ内の指定された数の結果をスキップしたりできます。

    $users = DB::table('users')->skip(10)->take(5)->get();

あるいは、`limit` メソッドと `offset` メソッドを使用することもできます。これらのメソッドは、それぞれ `take` メソッドおよび `skip` メソッドと機能的に同等です。

    $users = DB::table('users')
                    ->offset(10)
                    ->limit(5)
                    ->get();

<a name="conditional-clauses"></a>
## 条件節 (Conditional Clauses)

場合によっては、特定のクエリ句を別の条件に基づいてクエリに適用したい場合があります。たとえば、受信 HTTP リクエストに特定の入力値が存在する場合にのみ、`where` ステートメントを適用することができます。これは、`when` メソッドを使用して実行できます。

    $role = $request->input('role');

    $users = DB::table('users')
                    ->when($role, function ($query, $role) {
                        $query->where('role_id', $role);
                    })
                    ->get();

`when` メソッドは、最初の引数が `true` の場合にのみ、指定されたクロージャを実行します。最初の引数が `false` の場合、クロージャは実行されません。したがって、上記の例では、`when` メソッドに指定されたクロージャは、受信リクエストに `role` フィールドが存在し、`true` と評価される場合にのみ呼び出されます。

別のクロージャを `when` メソッドの 3 番目の引数として渡すことができます。このクロージャは、最初の引数が `false` として評価される場合にのみ実行されます。この機能がどのように使用されるかを説明するために、この機能を使用してクエリのデフォルトの順序を設定します。

    $sortByVotes = $request->input('sort_by_votes');

    $users = DB::table('users')
                    ->when($sortByVotes, function ($query, $sortByVotes) {
                        $query->orderBy('votes');
                    }, function ($query) {
                        $query->orderBy('name');
                    })
                    ->get();

<a name="insert-statements"></a>
## ステートメントの挿入 (Insert Statements)

クエリビルダは、データベース テーブルにレコードを挿入するために使用できる `insert` メソッドも提供します。 `insert` メソッドは、列名と値の配列を受け入れます。

    DB::table('users')->insert([
        'email' => 'kayla@example.com',
        'votes' => 0
    ]);

配列の配列を渡すことで、複数のレコードを一度に挿入できます。各配列は、テーブルに挿入する必要があるレコードを表します。

    DB::table('users')->insert([
        ['email' => 'picard@example.com', 'votes' => 0],
        ['email' => 'janeway@example.com', 'votes' => 0],
    ]);

`insertOrIgnore` メソッドは、データベースにレコードを挿入する際のエラーを無視します。この方法を使用する場合、重複レコード エラーは無視され、データベース エンジンによっては他の種類のエラーも無視される場合があることに注意してください。たとえば、`insertOrIgnore` は [MySQL の厳密モードをバイパスする](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution) になります。

    DB::table('users')->insertOrIgnore([
        ['id' => 1, 'email' => 'sisko@example.com'],
        ['id' => 2, 'email' => 'archer@example.com'],
    ]);

`insertUsing` メソッドは、サブクエリを使用して挿入するデータを決定しながら、テーブルに新しいレコードを挿入します。

    DB::table('pruned_users')->insertUsing([
        'id', 'name', 'email', 'email_verified_at'
    ], DB::table('users')->select(
        'id', 'name', 'email', 'email_verified_at'
    )->where('updated_at', '<=', now()->subMonth()));

<a name="auto-incrementing-ids"></a>
#### 自動インクリメントID

テーブルに自動インクリメント ID がある場合は、`insertGetId` メソッドを使用してレコードを挿入し、ID を取得します。

    $id = DB::table('users')->insertGetId(
        ['email' => 'john@example.com', 'votes' => 0]
    );

> **警告**
> PostgreSQL を使用する場合、`insertGetId` メソッドは、自動インクリメント列の名前が `id` であることを想定します。別の「シーケンス」から ID を取得したい場合は、列名を 2 番目のパラメーターとして `insertGetId` メソッドに渡すことができます。

<a name="upserts"></a>
### アップサート

`upsert` メソッドは、存在しないレコードを挿入し、指定した新しい値で既存のレコードを更新します。メソッドの最初の引数は挿入または更新する値で構成され、2 番目の引数は関連するテーブル内のレコードを一意に識別する列をリストします。このメソッドの 3 番目と最後の引数は、一致するレコードがデータベースにすでに存在する場合に更新する必要がある列の配列です。

    DB::table('flights')->upsert(
        [
            ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
            ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
        ],
        ['departure', 'destination'],
        ['price']
    );

上の例では、Laravel は 2 つのレコードを挿入しようとします。同じ `departure` 列値と `destination` 列値を持つレコードがすでに存在する場合、Laravel はそのレコードの `price` 列を更新します。

> **警告**
> SQL Server を除くすべてのデータベースでは、`upsert` メソッドの 2 番目の引数の列に「プライマリ」または「一意」インデックスが必要です。さらに、MySQL データベース ドライバは、`upsert` メソッドの 2 番目の引数を無視し、常にテーブルの「プライマリ」インデックスと「一意」インデックスを使用して既存のレコードを検出します。

<a name="update-statements"></a>
## 更新ステートメント (Update Statements)

クエリビルダは、データベースにレコードを挿入するだけでなく、`update` メソッドを使用して既存のレコードを更新することもできます。 `update` メソッドは、`insert` メソッドと同様に、更新される列を示す列と値のペアの配列を受け入れます。 `update` メソッドは、影響を受ける行の数を返します。 `where` 句を使用して、`update` クエリを制約できます。

    $affected = DB::table('users')
                  ->where('id', 1)
                  ->update(['votes' => 1]);

<a name="update-or-insert"></a>
#### 更新または挿入

場合によっては、データベース内の既存のレコードを更新したり、一致するレコードが存在しない場合にレコードを作成したりすることが必要な場合があります。このシナリオでは、`updateOrInsert` メソッドが使用される可能性があります。 `updateOrInsert` メソッドは、レコードを検索するための条件の配列と、更新される列を示す列と値のペアの配列という 2 つの引数を受け入れます。

`updateOrInsert` メソッドは、最初の引数の列と値のペアを使用して、一致するデータベース レコードの検索を試みます。レコードが存在する場合は、2 番目の引数の値で更新されます。レコードが見つからない場合は、両方の引数の属性を結合した新しいレコードが挿入されます。

    DB::table('users')
        ->updateOrInsert(
            ['email' => 'john@example.com', 'name' => 'John'],
            ['votes' => '2']
        );

<a name="updating-json-columns"></a>
### JSON列の更新

JSON 列を更新するときは、`->` 構文を使用して、JSON オブジェクト内の適切なキーを更新する必要があります。この操作は、MySQL 5.7 以降および PostgreSQL 9.5 以降でサポートされています。

    $affected = DB::table('users')
                  ->where('id', 1)
                  ->update(['options->enabled' => true]);

<a name="increment-and-decrement"></a>
### インクリメントとデクリメント

クエリビルダは、特定の列の値を増減する便利なメソッドも提供します。これらのメソッドは両方とも、少なくとも 1 つの引数、つまり変更する列を受け入れます。 2 番目の引数を指定して、列を増分または減分する量を指定できます。

    DB::table('users')->increment('votes');

    DB::table('users')->increment('votes', 5);

    DB::table('users')->decrement('votes');

    DB::table('users')->decrement('votes', 5);

必要に応じて、インクリメントまたはデクリメント操作中に更新する追加の列を指定することもできます。

    DB::table('users')->increment('votes', 1, ['name' => 'John']);

さらに、`incrementEach` および `decrementEach` メソッドを使用して、複数の列を一度に増加または減少させることができます。

    DB::table('users')->incrementEach([
        'votes' => 5,
        'balance' => 100,
    ]);

<a name="delete-statements"></a>
## ステートメントの削除 (Delete Statements)

クエリビルダの `delete` メソッドを使用して、テーブルからレコードを削除できます。 `delete` メソッドは、影響を受ける行の数を返します。 `delete` メソッドを呼び出す前に「where」句を追加することで、`delete` ステートメントを制約できます。

    $deleted = DB::table('users')->delete();

    $deleted = DB::table('users')->where('votes', '>', 100)->delete();

テーブル全体を切り詰める場合は、テーブルからすべてのレコードが削除され、自動インクリメント ID がゼロにリセットされます。`truncate` メソッドを使用できます。

    DB::table('users')->truncate();

<a name="table-truncation-and-postgresql"></a>
#### テーブルのトランケーションとPostgreSQL

PostgreSQL データベースを切り詰める場合、`CASCADE` 動作が適用されます。これは、他のテーブル内のすべての外部キー関連レコードも削除されることを意味します。

<a name="pessimistic-locking"></a>
## 悲観的ロック (Pessimistic Locking)

クエリビルダには、`select` ステートメントの実行時に「悲観的ロック」を実現するのに役立つ関数もいくつか含まれています。 「共有ロック」を使用してステートメントを実行するには、`sharedLock` メソッドを呼び出すことができます。共有ロックにより、トランザクションがコミットされるまで、選択された行は変更されなくなります。

    DB::table('users')
            ->where('votes', '>', 100)
            ->sharedLock()
            ->get();

あるいは、`lockForUpdate` メソッドを使用することもできます。 「更新用」ロックは、選択されたレコードが変更されたり、別の共有ロックで選択されたりすることを防ぎます。

    DB::table('users')
            ->where('votes', '>', 100)
            ->lockForUpdate()
            ->get();

<a name="debugging"></a>
## デバッグ (Debugging)

クエリの構築中に `dd` メソッドと `dump` メソッドを使用して、現在のクエリ バインディングと SQL をダンプできます。 `dd` メソッドはデバッグ情報を表示し、リクエストの実行を停止します。 `dump` メソッドはデバッグ情報を表示しますが、リクエストの実行は継続できます。

    DB::table('users')->where('votes', '>', 100)->dd();

    DB::table('users')->where('votes', '>', 100)->dump();

