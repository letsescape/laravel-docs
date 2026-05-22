# Eloquent: 人間関係 (Eloquent: Relationships)

- [Introduction](#introduction)
- [関係の定義](#defining-relationships)
    - [1対1](#one-to-one)
    - [1対多](#one-to-many)
    - [1 対多 (逆) / に属します](#one-to-many-inverse)
    - [多くのうちの 1 つを持っています](#has-one-of-many)
    - [ワンスルーあり](#has-one-through)
    - [スルーが多い](#has-many-through)
- [多対多の関係](#many-to-many)
    - [中間テーブル列の取得](#retrieving-intermediate-table-columns)
    - [中間テーブル列によるクエリのフィルタリング](#filtering-queries-via-intermediate-table-columns)
    - [中間テーブル列を使用したクエリの順序付け](#ordering-queries-via-intermediate-table-columns)
    - [カスタム中間テーブルモデルの定義](#defining-custom-intermediate-table-models)
- [ポリモーフィックな関係](#polymorphic-relationships)
    - [1対1](#one-to-one-polymorphic-relations)
    - [1対多](#one-to-many-polymorphic-relations)
    - [たくさんあるうちのひとつ](#one-of-many-polymorphic-relations)
    - [多対多](#many-to-many-polymorphic-relations)
    - [カスタム多態性型](#custom-polymorphic-types)
- [動的な関係](#dynamic-relationships)
- [関係のクエリ](#querying-relations)
    - [リレーションシップメソッドと動的プロパティ](#relationship-methods-vs-dynamic-properties)
    - [関係の存在のクエリ](#querying-relationship-existence)
    - [関係の不在のクエリ](#querying-relationship-absence)
    - [関係へのモーフのクエリ](#querying-morph-to-relationships)
- [関連モデルの集約](#aggregating-related-models)
    - [関連モデルのカウント](#counting-related-models)
    - [その他の集計関数](#other-aggregate-functions)
    - [Morph To Relationship で関連モデルをカウントする](#counting-related-models-on-morph-to-relationships)
- [熱心な読み込み](#eager-loading)
    - [熱心なロードの制限](#constraining-eager-loads)
    - [遅延熱心な読み込み](#lazy-eager-loading)
    - [遅延読み込みの防止](#preventing-lazy-loading)
- [関連モデルの挿入と更新](#inserting-and-updating-related-models)
    - [`save` メソッド](#the-save-method)
    - [`create` メソッド](#the-create-method)
    - [関係に属します](#updating-belongs-to-relationships)
    - [多対多の関係](#updating-many-to-many-relationships)
- [親のタイムスタンプに触れる](#touching-parent-timestamps)

<a name="introduction"></a>
## 導入 (Introduction)

多くの場合、データベース テーブルは相互に関連しています。たとえば、ブログ投稿に多くのコメントが含まれている場合や、注文がその投稿を行ったユーザーに関連している場合があります。 Eloquent を使用すると、これらの関係の管理と操作が簡単になり、さまざまな一般的な関係がサポートされます。

<div class="content-list" markdown="1">

- [1対1](#one-to-one)
- [1対多](#one-to-many)
- [多対多](#many-to-many)
- [ワンスルーあり](#has-one-through)
- [スルーが多い](#has-many-through)
- [1 対 1 (ポリモーフィック)](#one-to-one-polymorphic-relations)
- [1 対多 (ポリモーフィック)](#one-to-many-polymorphic-relations)
- [多対多 (ポリモーフィック)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 関係の定義 (Defining Relationships)

Eloquent リレーションシップは、Eloquent モデル クラスのメソッドとして定義されます。リレーションシップは強力な [クエリビルダ](/docs/{{version}}/queries) としても機能するため、リレーションシップをメソッドとして定義すると、強力なメソッド チェーン機能とクエリ機能が提供されます。たとえば、この `posts` 関係に追加のクエリ制約を連鎖させることができます。

    $user->posts()->where('active', 1)->get();

ただし、リレーションシップの使用について深く掘り下げる前に、Eloquent がサポートする各タイプのリレーションシップを定義する方法を学びましょう。

<a name="one-to-one"></a>
### 1対1

1 対 1 の関係は、非常に基本的なタイプのデータベース関係です。たとえば、`User` モデルは 1 つの `Phone` モデルに関連付けられる場合があります。この関係を定義するために、`phone` メソッドを `User` モデルに配置します。 `phone` メソッドは、`hasOne` メソッドを呼び出し、その結果を返す必要があります。 `hasOne` メソッドは、モデルの `Illuminate\Database\Eloquent\Model` 基本クラスを介してモデルで使用できます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\HasOne;

    class User extends Model
    {
        /**
         * Get the phone associated with the user.
         */
        public function phone(): HasOne
        {
            return $this->hasOne(Phone::class);
        }
    }

`hasOne` メソッドに渡される最初の引数は、関連するモデル クラスの名前です。関係が定義されたら、Eloquent の動的プロパティを使用して関連レコードを取得できます。動的プロパティを使用すると、モデル上で定義されたプロパティであるかのように、リレーションシップ メソッドにアクセスできます。

    $phone = User::find(1)->phone;

Eloquent は、親モデル名に基づいてリレーションシップの外部キーを決定します。この場合、`Phone` モデルには、`user_id` 外部キーがあると自動的に想定されます。この規則をオーバーライドしたい場合は、`hasOne` メソッドに 2 番目の引数を渡すことができます。

    return $this->hasOne(Phone::class, 'foreign_key');

さらに、Eloquent は、外部キーの値が親の主キー列と一致する必要があると想定しています。つまり、Eloquent は、`Phone` レコードの `user_id` 列でユーザーの `id` 列の値を検索します。リレーションシップで `id` またはモデルの `$primaryKey` プロパティ以外の主キー値を使用する場合は、3 番目の引数を `hasOne` メソッドに渡すことができます。

    return $this->hasOne(Phone::class, 'foreign_key', 'local_key');

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 逆関係の定義

したがって、`User` モデルから `Phone` モデルにアクセスできます。次に、電話機を所有するユーザーにアクセスできる関係を `Phone` モデルで定義しましょう。 `belongsTo` メソッドを使用して、`hasOne` 関係の逆を定義できます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsTo;

    class Phone extends Model
    {
        /**
         * Get the user that owns the phone.
         */
        public function user(): BelongsTo
        {
            return $this->belongsTo(User::class);
        }
    }

`user` メソッドを呼び出すと、Eloquent は、`Phone` モデルの `user_id` 列と一致する `id` を持つ `User` モデルを検索しようとします。

Eloquent は、リレーションシップ メソッドの名前を調べ、メソッド名の末尾に `_id` を付けることで、外部キー名を決定します。したがって、この場合、Eloquent は、`Phone` モデルに `user_id` 列があると想定します。ただし、`Phone` モデルの外部キーが `user_id` ではない場合は、カスタム キー名を 2 番目の引数として `belongsTo` メソッドに渡すことができます。

    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'foreign_key');
    }

親モデルが主キーとして `id` を使用していない場合、または別の列を使用して関連モデルを検索したい場合は、親テーブルのカスタム キーを指定する 3 番目の引数を `belongsTo` メソッドに渡すことができます。

    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
    }

<a name="one-to-many"></a>
### 1対多

1 対多の関係は、単一のモデルが 1 つ以上の子モデルの親となる関係を定義するために使用されます。たとえば、ブログ投稿には無限の数のコメントが含まれる場合があります。他のすべての Eloquent リレーションシップと同様に、1 対多のリレーションシップは、Eloquent モデルでメソッドを定義することによって定義されます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\HasMany;

    class Post extends Model
    {
        /**
         * Get the comments for the blog post.
         */
        public function comments(): HasMany
        {
            return $this->hasMany(Comment::class);
        }
    }

Eloquent は、`Comment` モデルに適切な外部キー列を自動的に決定することに注意してください。慣例により、Eloquent は親モデルの「スネーク ケース」名を取得し、接尾辞として `_id` を付けます。したがって、この例では、Eloquent は、`Comment` モデルの外部キー列が `post_id` であると想定します。

関係メソッドが定義されたら、`comments` プロパティにアクセスすることで、関連するコメントの [collection](/docs/{{version}}/eloquent-collections) にアクセスできます。 Eloquent は「動的なリレーションシップ プロパティ」を提供するため、モデル上のプロパティとして定義されているかのようにリレーションシップ メソッドにアクセスできることを思い出してください。

    use App\Models\Post;

    $comments = Post::find(1)->comments;

    foreach ($comments as $comment) {
        // ...
    }

すべてのリレーションシップはクエリビルダとしても機能するため、`comments` メソッドを呼び出してクエリに条件を連鎖させ続けることで、リレーションシップ クエリにさらに制約を追加できます。

    $comment = Post::find(1)->comments()
                        ->where('title', 'foo')
                        ->first();

`hasOne` メソッドと同様に、追加の引数を `hasMany` メソッドに渡すことで、外部キーとローカル キーをオーバーライドすることもできます。

    return $this->hasMany(Comment::class, 'foreign_key');

    return $this->hasMany(Comment::class, 'foreign_key', 'local_key');

<a name="one-to-many-inverse"></a>
### 1 対多 (逆) / に属します

投稿のすべてのコメントにアクセスできるようになったので、コメントが親投稿にアクセスできるように関係を定義しましょう。 `hasMany` リレーションシップの逆を定義するには、`belongsTo` メソッドを呼び出すリレーションシップ メソッドを子モデルに定義します。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsTo;

    class Comment extends Model
    {
        /**
         * Get the post that owns the comment.
         */
        public function post(): BelongsTo
        {
            return $this->belongsTo(Post::class);
        }
    }

関係が定義されたら、`post` の「動的関係プロパティ」にアクセスして、コメントの親投稿を取得できます。

    use App\Models\Comment;

    $comment = Comment::find(1);

    return $comment->post->title;

上記の例では、Eloquent は、`Comment` モデルの `post_id` 列と一致する `id` を持つ `Post` モデルを検索しようとします。

Eloquent は、リレーションシップ メソッドの名前を調べ、メソッド名の末尾に `_` を付け、その後に親モデルの主キー列の名前を付けることで、デフォルトの外部キー名を決定します。したがって、この例では、Eloquent は、`comments` テーブル上の `Post` モデルの外部キーが `post_id` であると想定します。

ただし、リレーションシップの外部キーがこれらの規則に従っていない場合は、カスタム外部キー名を `belongsTo` メソッドの 2 番目の引数として渡すことができます。

    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class, 'foreign_key');
    }

親モデルが主キーとして `id` を使用していない場合、または別の列を使用して関連モデルを検索したい場合は、親テーブルのカスタム キーを指定する 3 番目の引数を `belongsTo` メソッドに渡すことができます。

    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
    }

<a name="default-models"></a>
#### デフォルトのモデル

`belongsTo`、`hasOne`、`hasOneThrough`、および `morphOne` 関係を使用すると、指定された関係が `null` の場合に返されるデフォルト モデルを定義できます。このパターンは [ヌルオブジェクトパターン](https://en.wikipedia.org/wiki/Null_Object_pattern) と呼ばれることが多く、コード内の条件チェックを削除するのに役立ちます。次の例では、`Post` モデルにユーザーがアタッチされていない場合、`user` リレーションは空の `App\Models\User` モデルを返します。

    /**
     * Get the author of the post.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class)->withDefault();
    }

デフォルトのモデルに属性を設定するには、配列またはクロージャを `withDefault` メソッドに渡すことができます。

    /**
     * Get the author of the post.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class)->withDefault([
            'name' => 'Guest Author',
        ]);
    }

    /**
     * Get the author of the post.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
            $user->name = 'Guest Author';
        });
    }

<a name="querying-belongs-to-relationships"></a>
#### クエリは関係に属します

「belongs to」関係の子をクエリする場合、`where` 句を手動で構築して、対応する Eloquent モデルを取得できます。

    use App\Models\Post;

    $posts = Post::where('user_id', $user->id)->get();

ただし、指定されたモデルの適切な関係と外部キーを自動的に決定する `whereBelongsTo` メソッドを使用する方が便利な場合があります。

    $posts = Post::whereBelongsTo($user)->get();

[collection](/docs/{{version}}/eloquent-collections) インスタンスを `whereBelongsTo` メソッドに提供することもできます。これを行うと、Laravel はコレクション内のいずれかの親モデルに属するモデルを取得します。

    $users = User::where('vip', true)->get();

    $posts = Post::whereBelongsTo($users)->get();

デフォルトでは、Laravel はモデルのクラス名に基づいて、指定されたモデルに関連付けられた関係を決定します。ただし、関係名を `whereBelongsTo` メソッドの 2 番目の引数として指定することで、手動で指定することもできます。

    $posts = Post::whereBelongsTo($user, 'author')->get();

<a name="has-one-of-many"></a>
### 多くのうちの 1 つを持っています

場合によっては、モデルに多数の関連モデルがある場合でも、関係の「最新」または「最も古い」関連モデルを簡単に取得したいことがあります。たとえば、`User` モデルは多くの `Order` モデルに関連している可能性がありますが、ユーザーが行った最新の注文を操作する便利な方法を定義したいとします。これは、`hasOne` 関係タイプと `ofMany` メソッドを組み合わせて使用​​することで実現できます。

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

同様に、関係の「最も古い」つまり最初の関連モデルを取得するメソッドを定義できます。

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

デフォルトでは、`latestOfMany` メソッドと `oldestOfMany` メソッドは、モデルの主キーに基づいて最新または最も古い関連モデルを取得します。これは並べ替え可能である必要があります。ただし、異なる並べ替え基準を使用して、より大きな関係から単一のモデルを取得したい場合があります。

たとえば、`ofMany` メソッドを使用すると、ユーザーの最も高価な注文を取得できます。 `ofMany` メソッドは、最初の引数としてソート可能な列を受け入れ、関連モデルのクエリを実行するときに適用する集計関数 (`min` または `max`) を受け取ります。

```php
/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]  
> PostgreSQL は UUID 列に対する `MAX` 関数の実行をサポートしていないため、現時点では、PostgreSQL UUID 列と組み合わせて 1/2 リレーションシップを使用することはできません。

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### 「多数」の関係を 1 つの関係に変換する

`latestOfMany`、`oldestOfMany`、または `ofMany` メソッドを使用して単一のモデルを取得する場合、多くの場合、同じモデルに対して「多数を持つ」関係がすでに定義されています。便宜上、Laravel では、関係に対して `one` メソッドを呼び出すことで、この関係を「has one」関係に簡単に変換できます。

```php
/**
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### アドバンストは多くの関係のうちの 1 つを持っています

より高度な「多数のうちの 1 つを有する」関係を構築することが可能です。たとえば、`Product` モデルには、新しい価格が公開された後でもシステムに保持される多くの関連する `Price` モデルがある場合があります。さらに、製品の新しい価格データを事前に公開して、`published_at` 列を介して将来の日付に有効にすることができる場合があります。

したがって、要約すると、公開日が将来ではない最新の公開価格を取得する必要があります。さらに、2 つの価格の発行日が同じ場合は、ID が最も大きい価格が優先されます。これを実現するには、最新の価格を決定する並べ替え可能な列を含む配列を `ofMany` メソッドに渡す必要があります。さらに、クロージャは `ofMany` メソッドの 2 番目の引数として提供されます。このクロージャは、リレーションシップ クエリに追加の公開日制約を追加する役割を果たします。

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### ワンスルーあり

「has-one-through」関係は、別のモデルとの 1 対 1 の関係を定義します。ただし、この関係は、3 番目のモデルを通過することで、宣言モデルを別のモデルの 1 つのインスタンスと照合できることを示しています。

たとえば、自動車修理工場アプリケーションでは、各 `Mechanic` モデルが 1 つの `Car` モデルに関連付けられ、各 `Car` モデルが 1 つの `Owner` モデルに関連付けられる場合があります。整備士と所有者にはデータベース内で直接の関係はありませんが、整備士は `Car` モデルを介して所有者にアクセスできます。この関係を定義するために必要なテーブルを見てみましょう。

    mechanics
        id - integer
        name - string

    cars
        id - integer
        model - string
        mechanic_id - integer

    owners
        id - integer
        name - string
        car_id - integer

リレーションシップのテーブル構造を調べたので、`Mechanic` モデルでリレーションシップを定義しましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\HasOneThrough;

    class Mechanic extends Model
    {
        /**
         * Get the car's owner.
         */
        public function carOwner(): HasOneThrough
        {
            return $this->hasOneThrough(Owner::class, Car::class);
        }
    }

`hasOneThrough` メソッドに渡される最初の引数はアクセスする最終モデルの名前であり、2 番目の引数は中間モデルの名前です。

または、関連するリレーションシップがそのリレーションシップに関与するすべてのモデルですでに定義されている場合は、`through` メソッドを呼び出してそれらのリレーションシップの名前を指定することによって、「has-one-through」リレーションシップをスムーズに定義できます。たとえば、`Mechanic` モデルに `cars` 関係があり、`Car` モデルに `owner` 関係がある場合、次のように整備士と所有者を接続する「has-one-through」関係を定義できます。

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 主な規約

関係のクエリを実行するときは、一般的な Eloquent 外部キー規則が使用されます。関係のキーをカスタマイズしたい場合は、それらを `hasOneThrough` メソッドの 3 番目と 4 番目の引数として渡すことができます。 3 番目の引数は、中間モデルの外部キーの名前です。 4 番目の引数は、最終モデルの外部キーの名前です。 5 番目の引数はローカル キーであり、6 番目の引数は中間モデルのローカル キーです。

    class Mechanic extends Model
    {
        /**
         * Get the car's owner.
         */
        public function carOwner(): HasOneThrough
        {
            return $this->hasOneThrough(
                Owner::class,
                Car::class,
                'mechanic_id', // Foreign key on the cars table...
                'car_id', // Foreign key on the owners table...
                'id', // Local key on the mechanics table...
                'id' // Local key on the cars table...
            );
        }
    }

または、前に説明したように、関係に関係するすべてのモデルで関連する関係がすでに定義されている場合は、`through` メソッドを呼び出してそれらの関係の名前を指定することによって、「has-one-through」関係をスムーズに定義できます。このアプローチには、既存の関係ですでに定義されている主要な規則を再利用できるという利点があります。

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### スルーが多い

「has-many-through」関係は、中間関係を介して離れた関係にアクセスする便利な方法を提供します。たとえば、[Laravel Vapor](https://vapor.laravel.com) のような展開プラットフォームを構築していると仮定します。 `Project` モデルは、中間の `Environment` モデルを介して多くの `Deployment` モデルにアクセスする可能性があります。この例を使用すると、特定のプロジェクトのすべてのデプロイメントを簡単に収集できます。この関係を定義するために必要なテーブルを見てみましょう。

    projects
        id - integer
        name - string

    environments
        id - integer
        project_id - integer
        name - string

    deployments
        id - integer
        environment_id - integer
        commit_hash - string

リレーションシップのテーブル構造を調べたので、`Project` モデルでリレーションシップを定義しましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\HasManyThrough;

    class Project extends Model
    {
        /**
         * Get all of the deployments for the project.
         */
        public function deployments(): HasManyThrough
        {
            return $this->hasManyThrough(Deployment::class, Environment::class);
        }
    }

`hasManyThrough` メソッドに渡される最初の引数はアクセスする最終モデルの名前であり、2 番目の引数は中間モデルの名前です。

または、関連するリレーションシップがそのリレーションシップに関与するすべてのモデルですでに定義されている場合は、`through` メソッドを呼び出してそれらのリレーションシップの名前を指定することで、「has-many-through」リレーションシップをスムーズに定義できます。たとえば、`Project` モデルに `environments` 関係があり、`Environment` モデルに `deployments` 関係がある場合、プロジェクトとデプロイメントを接続する「has-many-through」関係を次のように定義できます。

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` モデルのテーブルには `project_id` 列が含まれていませんが、`hasManyThrough` リレーションにより、`$project->deployments` を介してプロジェクトのデプロイメントへのアクセスが提供されます。これらのモデルを取得するために、Eloquent は中間 `Environment` モデルのテーブルの `project_id` 列を検査します。関連する環境 ID を見つけた後、それらを使用して `Deployment` モデルのテーブルをクエリします。

<a name="has-many-through-key-conventions"></a>
#### 主な規約

関係のクエリを実行するときは、一般的な Eloquent 外部キー規則が使用されます。関係のキーをカスタマイズしたい場合は、それらを `hasManyThrough` メソッドの 3 番目と 4 番目の引数として渡すことができます。 3 番目の引数は、中間モデルの外部キーの名前です。 4 番目の引数は、最終モデルの外部キーの名前です。 5 番目の引数はローカル キーであり、6 番目の引数は中間モデルのローカル キーです。

    class Project extends Model
    {
        public function deployments(): HasManyThrough
        {
            return $this->hasManyThrough(
                Deployment::class,
                Environment::class,
                'project_id', // Foreign key on the environments table...
                'environment_id', // Foreign key on the deployments table...
                'id', // Local key on the projects table...
                'id' // Local key on the environments table...
            );
        }
    }

または、前に説明したように、関係に関係するすべてのモデルで関連する関係がすでに定義されている場合は、`through` メソッドを呼び出してそれらの関係の名前を指定することによって、「has-many-through」関係をスムーズに定義できます。このアプローチには、既存の関係ですでに定義されている主要な規則を再利用できるという利点があります。

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="many-to-many"></a>
## 多対多の関係 (Many to Many Relationships)

多対多のリレーションは、`hasOne` および `hasMany` のリレーションよりも少し複雑です。多対多の関係の例としては、ユーザーが多くのロールを持ち、それらのロールがアプリケーション内の他のユーザーによって共有される場合があります。たとえば、ユーザーに「作成者」と「編集者」の役割を割り当てることができます。ただし、これらの役割は他のユーザーにも割り当てられる場合があります。したがって、ユーザーには多くのロールがあり、ロールには多くのユーザーが含まれます。

<a name="many-to-many-table-structure"></a>
#### テーブル構造

この関係を定義するには、`users`、`roles`、および `role_user` の 3 つのデータベース テーブルが必要です。 `role_user` テーブルは、関連するモデル名のアルファベット順から派生し、`user_id` 列と `role_id` 列が含まれます。このテーブルは、ユーザーとロールを結び付ける中間テーブルとして使用されます。

ロールは多くのユーザーに属することができるため、単純に `user_id` 列を `roles` テーブルに配置することはできないことに注意してください。これは、ロールは 1 人のユーザーにのみ属することができることを意味します。複数のユーザーに割り当てられるロールのサポートを提供するには、`role_user` テーブルが必要です。リレーションシップのテーブル構造は次のように要約できます。

    users
        id - integer
        name - string

    roles
        id - integer
        name - string

    role_user
        user_id - integer
        role_id - integer

<a name="many-to-many-model-structure"></a>
#### モデルの構造

多対多の関係は、`belongsToMany` メソッドの結果を返すメソッドを作成することによって定義されます。 `belongsToMany` メソッドは、アプリケーションのすべての Eloquent モデルで使用される `Illuminate\Database\Eloquent\Model` 基本クラスによって提供されます。たとえば、`User` モデルで `roles` メソッドを定義してみましょう。このメソッドに渡される最初の引数は、関連するモデル クラスの名前です。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsToMany;

    class User extends Model
    {
        /**
         * The roles that belong to the user.
         */
        public function roles(): BelongsToMany
        {
            return $this->belongsToMany(Role::class);
        }
    }

関係が定義されたら、`roles` 動的関係プロパティを使用してユーザーのロールにアクセスできます。

    use App\Models\User;

    $user = User::find(1);

    foreach ($user->roles as $role) {
        // ...
    }

すべてのリレーションシップはクエリビルダとしても機能するため、`roles` メソッドを呼び出してクエリに条件を連鎖させ続けることで、リレーションシップ クエリにさらに制約を追加できます。

    $roles = User::find(1)->roles()->orderBy('name')->get();

リレーションシップの中間テーブルのテーブル名を決定するために、Eloquent は 2 つの関連するモデル名をアルファベット順に結合します。ただし、この規則は自由にオーバーライドできます。これを行うには、2 番目の引数を `belongsToMany` メソッドに渡します。

    return $this->belongsToMany(Role::class, 'role_user');

中間テーブルの名前をカスタマイズするだけでなく、追加の引数を `belongsToMany` メソッドに渡すことで、テーブルのキーの列名もカスタマイズできます。 3 番目の引数はリレーションシップを定義するモデルの外部キー名で、4 番目の引数は結合先のモデルの外部キー名です。

    return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 逆関係の定義

多対多の関係の「逆」を定義するには、`belongsToMany` メソッドの結果も返す関連モデル上でメソッドを定義する必要があります。ユーザー/ロールの例を完成させるために、`Role` モデルで `users` メソッドを定義しましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsToMany;

    class Role extends Model
    {
        /**
         * The users that belong to the role.
         */
        public function users(): BelongsToMany
        {
            return $this->belongsToMany(User::class);
        }
    }

ご覧のとおり、関係は、`App\Models\User` モデルの参照を除き、対応する `User` モデルとまったく同じように定義されています。 `belongsToMany` メソッドを再利用しているため、多対多のリレーションシップの「逆」を定義するときに、通常のテーブルとキーのカスタマイズ オプションがすべて利用可能です。

<a name="retrieving-intermediate-table-columns"></a>
### 中間テーブル列の取得

すでに学習したように、多対多のリレーションを操作するには、中間テーブルの存在が必要です。 Eloquent は、このテーブルを操作するための非常に役立つ方法をいくつか提供します。たとえば、`User` モデルに関連する `Role` モデルが多数あると仮定します。このリレーションシップにアクセスした後、モデルの `pivot` 属性を使用して中間テーブルにアクセスできます。

    use App\Models\User;

    $user = User::find(1);

    foreach ($user->roles as $role) {
        echo $role->pivot->created_at;
    }

取得した各 `Role` モデルには、自動的に `pivot` 属性が割り当てられることに注意してください。この属性には、中間テーブルを表すモデルが含まれています。

デフォルトでは、`pivot` モデルにはモデル キーのみが存在します。中間テーブルに追加の属性が含まれている場合は、リレーションシップを定義するときにそれらを指定する必要があります。

    return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');

中間テーブルに Eloquent によって自動的に維持される `created_at` および `updated_at` タイムスタンプを持たせたい場合は、関係を定義するときに `withTimestamps` メソッドを呼び出します。

    return $this->belongsToMany(Role::class)->withTimestamps();

> [!WARNING]  
> Eloquent の自動的に維持されるタイムスタンプを利用する中間テーブルには、`created_at` と `updated_at` の両方のタイムスタンプ列が必要です。

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 属性名のカスタマイズ

前述したように、中間テーブルの属性には、`pivot` 属性を介してモデル上でアクセスできます。ただし、アプリケーション内での目的をより適切に反映するために、この属性の名前を自由にカスタマイズできます。

たとえば、アプリケーションにポッドキャストを購読する可能性のあるユーザーが含まれている場合、ユーザーとポッドキャストの間に多対多の関係が存在する可能性があります。この場合、中間テーブル属性の名前を `pivot` ではなく `subscription` に変更するとよいでしょう。これは、関係を定義するときに `as` メソッドを使用して行うことができます。

    return $this->belongsToMany(Podcast::class)
                    ->as('subscription')
                    ->withTimestamps();

カスタム中間テーブル属性を指定すると、カスタマイズされた名前を使用して中間テーブル データにアクセスできます。

    $users = User::with('podcasts')->get();

    foreach ($users->flatMap->podcasts as $podcast) {
        echo $podcast->subscription->created_at;
    }

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 中間テーブル列によるクエリのフィルタリング

関係を定義するときに、`wherePivot`、`wherePivotIn`、`wherePivotNotIn`、`wherePivotBetween`、`wherePivotNotBetween`、`wherePivotNull`、および `wherePivotNotNull` メソッドを使用して、`belongsToMany` 関係クエリによって返された結果をフィルターすることもできます。

    return $this->belongsToMany(Role::class)
                    ->wherePivot('approved', 1);

    return $this->belongsToMany(Role::class)
                    ->wherePivotIn('priority', [1, 2]);

    return $this->belongsToMany(Role::class)
                    ->wherePivotNotIn('priority', [1, 2]);

    return $this->belongsToMany(Podcast::class)
                    ->as('subscriptions')
                    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

    return $this->belongsToMany(Podcast::class)
                    ->as('subscriptions')
                    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

    return $this->belongsToMany(Podcast::class)
                    ->as('subscriptions')
                    ->wherePivotNull('expired_at');

    return $this->belongsToMany(Podcast::class)
                    ->as('subscriptions')
                    ->wherePivotNotNull('expired_at');

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 中間テーブル列を使用したクエリの順序付け

`orderByPivot` メソッドを使用して、`belongsToMany` 関係クエリによって返された結果を並べ替えることができます。次の例では、ユーザーの最新のバッジをすべて取得します。

    return $this->belongsToMany(Badge::class)
                    ->where('rank', 'gold')
                    ->orderByPivot('created_at', 'desc');

<a name="defining-custom-intermediate-table-models"></a>
### カスタム中間テーブルモデルの定義

多対多のリレーションシップの中間テーブルを表すカスタム モデルを定義したい場合は、リレーションシップを定義するときに `using` メソッドを呼び出すことができます。カスタム ピボット モデルを使用すると、ピボット モデルでメソッドやキャストなどの追加の動作を定義できます。

カスタム多対多ピボット モデルは `Illuminate\Database\Eloquent\Relations\Pivot` クラスを拡張する必要があり、カスタムの多態性多対多ピボット モデルは `Illuminate\Database\Eloquent\Relations\MorphPivot` クラスを拡張する必要があります。たとえば、カスタム `RoleUser` ピボット モデルを使用する `Role` モデルを定義できます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsToMany;

    class Role extends Model
    {
        /**
         * The users that belong to the role.
         */
        public function users(): BelongsToMany
        {
            return $this->belongsToMany(User::class)->using(RoleUser::class);
        }
    }

`RoleUser` モデルを定義するときは、`Illuminate\Database\Eloquent\Relations\Pivot` クラスを拡張する必要があります。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Relations\Pivot;

    class RoleUser extends Pivot
    {
        // ...
    }

> [!WARNING]  
> ピボット モデルは、`SoftDeletes` 特性を使用できない場合があります。ピボット レコードをソフト デリートする必要がある場合は、ピボット モデルを実際の Eloquent モデルに変換することを検討してください。

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### カスタム ピボット モデルと増分 ID

カスタム ピボット モデルを使用する多対多のリレーションシップを定義しており、そのピボット モデルに自動インクリメント主キーがある場合は、カスタム ピボット モデル クラスで、`true` に設定された `incrementing` プロパティが定義されていることを確認する必要があります。

    /**
     * Indicates if the IDs are auto-incrementing.
     *
     * @var bool
     */
    public $incrementing = true;

<a name="polymorphic-relationships"></a>
## ポリモーフィックな関係 (Polymorphic Relationships)

ポリモーフィックな関係により、子モデルは単一の関連付けを使用して複数のタイプのモデルに属することができます。たとえば、ユーザーがブログ投稿やビデオを共有できるアプリケーションを構築していると想像してください。このようなアプリケーションでは、`Comment` モデルが `Post` モデルと `Video` モデルの両方に属する可能性があります。

<a name="one-to-one-polymorphic-relations"></a>
### 1 対 1 (ポリモーフィック)

<a name="one-to-one-polymorphic-table-structure"></a>
#### テーブル構造

1 対 1 の多態性リレーションは、典型的な 1 対 1 のリレーションと似ています。ただし、子モデルは、単一の関連付けを使用して複数のタイプのモデルに属することができます。たとえば、ブログ `Post` と `User` は、`Image` モデルとの多態性関係を共有する場合があります。 1 対 1 のポリモーフィックな関係を使用すると、投稿やユーザーに関連付けられる一意の画像を含む単一のテーブルを作成できます。まず、テーブル構造を調べてみましょう。

    posts
        id - integer
        name - string

    users
        id - integer
        name - string

    images
        id - integer
        url - string
        imageable_id - integer
        imageable_type - string

`images` テーブルの `imageable_id` 列と `imageable_type` 列に注目してください。 `imageable_id` 列には投稿またはユーザーの ID 値が含まれ、`imageable_type` 列には親モデルのクラス名が含まれます。 `imageable_type` 列は、`imageable` リレーションにアクセスするときに、親モデルのどの「タイプ」を返すかを決定するために Eloquent によって使用されます。この場合、列には `App\Models\Post` または `App\Models\User` のいずれかが含まれます。

<a name="one-to-one-polymorphic-model-structure"></a>
#### モデルの構造

次に、この関係を構築するために必要なモデル定義を調べてみましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphTo;

    class Image extends Model
    {
        /**
         * Get the parent imageable model (user or post).
         */
        public function imageable(): MorphTo
        {
            return $this->morphTo();
        }
    }

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphOne;

    class Post extends Model
    {
        /**
         * Get the post's image.
         */
        public function image(): MorphOne
        {
            return $this->morphOne(Image::class, 'imageable');
        }
    }

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphOne;

    class User extends Model
    {
        /**
         * Get the user's image.
         */
        public function image(): MorphOne
        {
            return $this->morphOne(Image::class, 'imageable');
        }
    }

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 関係の取得

データベースのテーブルとモデルを定義したら、モデルを介してリレーションシップにアクセスできるようになります。たとえば、投稿の画像を取得するには、`image` 動的関係プロパティにアクセスします。

    use App\Models\Post;

    $post = Post::find(1);

    $image = $post->image;

`morphTo` への呼び出しを実行するメソッドの名前にアクセスすることで、多態性モデルの親を取得できます。この場合、それは `Image` モデルの `imageable` メソッドです。したがって、動的関係プロパティとしてそのメソッドにアクセスします。

    use App\Models\Image;

    $image = Image::find(1);

    $imageable = $image->imageable;

`Image` モデルの `imageable` リレーションは、イメージを所有するモデルのタイプに応じて、`Post` インスタンスまたは `User` インスタンスを返します。

<a name="morph-one-to-one-key-conventions"></a>
#### 主な規約

必要に応じて、多態性子モデルで使用される「id」列と「type」列の名前を指定できます。その場合は、常にリレーションシップの名前を最初の引数として `morphTo` メソッドに渡すようにしてください。通常、この値はメソッド名と一致する必要があるため、PHP の `__FUNCTION__` 定数を使用できます。

    /**
     * Get the model that the image belongs to.
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
    }

<a name="one-to-many-polymorphic-relations"></a>
### 1 対多 (ポリモーフィック)

<a name="one-to-many-polymorphic-table-structure"></a>
#### テーブル構造

1 対多のポリモーフィックな関係は、典型的な 1 対多の関係と似ています。ただし、子モデルは、単一の関連付けを使用して複数のタイプのモデルに属することができます。たとえば、アプリケーションのユーザーが投稿やビデオに「コメント」できると想像してください。ポリモーフィックな関係を使用すると、単一の `comments` テーブルを使用して、投稿とビデオの両方のコメントを含めることができます。まず、この関係を構築するために必要なテーブル構造を調べてみましょう。

    posts
        id - integer
        title - string
        body - text

    videos
        id - integer
        title - string
        url - string

    comments
        id - integer
        body - text
        commentable_id - integer
        commentable_type - string

<a name="one-to-many-polymorphic-model-structure"></a>
#### モデルの構造

次に、この関係を構築するために必要なモデル定義を調べてみましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphTo;

    class Comment extends Model
    {
        /**
         * Get the parent commentable model (post or video).
         */
        public function commentable(): MorphTo
        {
            return $this->morphTo();
        }
    }

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphMany;

    class Post extends Model
    {
        /**
         * Get all of the post's comments.
         */
        public function comments(): MorphMany
        {
            return $this->morphMany(Comment::class, 'commentable');
        }
    }

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphMany;

    class Video extends Model
    {
        /**
         * Get all of the video's comments.
         */
        public function comments(): MorphMany
        {
            return $this->morphMany(Comment::class, 'commentable');
        }
    }

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 関係の取得

データベース テーブルとモデルを定義したら、モデルの動的関係プロパティを介して関係にアクセスできます。たとえば、投稿のすべてのコメントにアクセスするには、`comments` 動的プロパティを使用できます。

    use App\Models\Post;

    $post = Post::find(1);

    foreach ($post->comments as $comment) {
        // ...
    }

`morphTo` への呼び出しを実行するメソッドの名前にアクセスして、多態性子モデルの親を取得することもできます。この場合、それは `Comment` モデルの `commentable` メソッドです。したがって、コメントの親モデルにアクセスするために、動的関係プロパティとしてそのメソッドにアクセスします。

    use App\Models\Comment;

    $comment = Comment::find(1);

    $commentable = $comment->commentable;

`Comment` モデルの `commentable` リレーションは、コメントの親であるモデルのタイプに応じて、`Post` インスタンスまたは `Video` インスタンスを返します。

<a name="one-of-many-polymorphic-relations"></a>
### 多数のうちの 1 つ (ポリモーフィック)

場合によっては、モデルに多数の関連モデルがある場合でも、関係の「最新」または「最も古い」関連モデルを簡単に取得したいことがあります。たとえば、`User` モデルは多くの `Image` モデルに関連している可能性がありますが、ユーザーがアップロードした最新の画像を操作する便利な方法を定義したいとします。これは、`morphOne` 関係タイプと `ofMany` メソッドを組み合わせて使用​​することで実現できます。

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

同様に、関係の「最も古い」つまり最初の関連モデルを取得するメソッドを定義できます。

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

デフォルトでは、`latestOfMany` メソッドと `oldestOfMany` メソッドは、モデルの主キーに基づいて最新または最も古い関連モデルを取得します。これは並べ替え可能である必要があります。ただし、異なる並べ替え基準を使用して、より大きな関係から単一のモデルを取得したい場合があります。

たとえば、`ofMany` メソッドを使用すると、ユーザーが最も「気に入った」画像を取得できます。 `ofMany` メソッドは、最初の引数としてソート可能な列を受け入れ、関連モデルのクエリを実行するときに適用する集計関数 (`min` または `max`) を受け取ります。

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]  
> より高度な「多数の中の一つ」の関係を構築することが可能です。詳細については、[多くのドキュメントのうちの 1 つを持っています](#advanced-has-one-of-many-relationships) を参照してください。

<a name="many-to-many-polymorphic-relations"></a>
### 多対多 (ポリモーフィック)

<a name="many-to-many-polymorphic-table-structure"></a>
#### テーブル構造

多対多のポリモーフィック リレーションは、「モーフ 1」および「モーフ メニー」リレーションシップよりも少し複雑です。たとえば、`Post` モデルと `Video` モデルは、`Tag` モデルに対する多態性リレーションを共有できます。この状況で多対多のポリモーフィックな関係を使用すると、アプリケーションは投稿やビデオに関連付けられる可能性のある一意のタグの単一のテーブルを持つことができます。まず、この関係を構築するために必要なテーブル構造を調べてみましょう。

    posts
        id - integer
        name - string

    videos
        id - integer
        name - string

    tags
        id - integer
        name - string

    taggables
        tag_id - integer
        taggable_id - integer
        taggable_type - string

> [!NOTE]  
> ポリモーフィックな多対多の関係に入る前に、一般的な [多対多の関係](#many-to-many) に関するドキュメントを読むと役に立つ場合があります。

<a name="many-to-many-polymorphic-model-structure"></a>
#### モデルの構造

次に、モデル上の関係を定義する準備が整います。 `Post` モデルと `Video` モデルには両方とも、基本 Eloquent モデル クラスによって提供される `morphToMany` メソッドを呼び出す `tags` メソッドが含まれます。

`morphToMany` メソッドは、関連モデルの名前と「関係名」を受け入れます。中間テーブル名に割り当てた名前とそれに含まれるキーに基づいて、この関係を「タグ付け可能」と呼びます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphToMany;

    class Post extends Model
    {
        /**
         * Get all of the tags for the post.
         */
        public function tags(): MorphToMany
        {
            return $this->morphToMany(Tag::class, 'taggable');
        }
    }

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 逆関係の定義

次に、`Tag` モデルで、考えられる親モデルごとにメソッドを定義する必要があります。したがって、この例では、`posts` メソッドと `videos` メソッドを定義します。これらのメソッドは両方とも、`morphedByMany` メソッドの結果を返す必要があります。

`morphedByMany` メソッドは、関連モデルの名前と「関係名」を受け入れます。中間テーブル名に割り当てた名前とそれに含まれるキーに基づいて、この関係を「タグ付け可能」と呼びます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphToMany;

    class Tag extends Model
    {
        /**
         * Get all of the posts that are assigned this tag.
         */
        public function posts(): MorphToMany
        {
            return $this->morphedByMany(Post::class, 'taggable');
        }

        /**
         * Get all of the videos that are assigned this tag.
         */
        public function videos(): MorphToMany
        {
            return $this->morphedByMany(Video::class, 'taggable');
        }
    }

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 関係の取得

データベースのテーブルとモデルを定義したら、モデルを介してリレーションシップにアクセスできるようになります。たとえば、投稿のすべてのタグにアクセスするには、`tags` 動的関係プロパティを使用できます。

    use App\Models\Post;

    $post = Post::find(1);

    foreach ($post->tags as $tag) {
        // ...
    }

`morphedByMany` への呼び出しを実行するメソッドの名前にアクセスすることで、多態性子モデルから多態性関係の親を取得できます。この場合、それは `Tag` モデルの `posts` メソッドまたは `videos` メソッドです。

    use App\Models\Tag;

    $tag = Tag::find(1);

    foreach ($tag->posts as $post) {
        // ...
    }

    foreach ($tag->videos as $video) {
        // ...
    }

<a name="custom-polymorphic-types"></a>
### カスタム多態性型

デフォルトでは、Laravel は完全修飾クラス名を使用して関連モデルの「タイプ」を保存します。たとえば、`Comment` モデルが `Post` モデルまたは `Video` モデルに属する上記の 1 対多の関係の例を考えると、デフォルトの `commentable_type` はそれぞれ `App\Models\Post` または `App\Models\Video` になります。ただし、これらの値をアプリケーションの内部構造から切り離したい場合があります。

たとえば、「タイプ」としてモデル名を使用する代わりに、`post` や `video` などの単純な文字列を使用することもできます。そうすることで、モデルの名前が変更されても、データベース内の多態性の「type」列の値は有効なままになります。

    use Illuminate\Database\Eloquent\Relations\Relation;

    Relation::enforceMorphMap([
        'post' => 'App\Models\Post',
        'video' => 'App\Models\Video',
    ]);

必要に応じて、`App\Providers\AppServiceProvider` クラスの `boot` メソッドで `enforceMorphMap` メソッドを呼び出すことも、別のサービスプロバイダを作成することもできます。

モデルの `getMorphClass` メソッドを使用して、実行時に特定のモデルのモーフ エイリアスを決定できます。逆に、`Relation::getMorphedModel` メソッドを使用して、モーフ エイリアスに関連付けられた完全修飾クラス名を決定することもできます。

    use Illuminate\Database\Eloquent\Relations\Relation;

    $alias = $post->getMorphClass();

    $class = Relation::getMorphedModel($alias);

> [!WARNING]  
> 既存のアプリケーションに「モーフ マップ」を追加する場合、完全修飾クラスがまだ含まれているデータベース内のすべてのモーフィング可能な `*_type` 列値をその「マップ」名に変換する必要があります。

<a name="dynamic-relationships"></a>
### 動的な関係

`resolveRelationUsing` メソッドを使用して、実行時に Eloquent モデル間の関係を定義できます。通常のアプリケーション開発には通常推奨されませんが、Laravel パッケージを開発する場合にはこれが役立つ場合があります。

`resolveRelationUsing` メソッドは、最初の引数として必要な関係名を受け入れます。メソッドに渡される 2 番目の引数は、モデル インスタンスを受け入れ、有効な Eloquent リレーションシップ定義を返すクロージャである必要があります。通常、[サービスプロバイダ](/docs/{{version}}/providers) のブート メソッド内で動的関係を構成する必要があります。

    use App\Models\Order;
    use App\Models\Customer;

    Order::resolveRelationUsing('customer', function (Order $orderModel) {
        return $orderModel->belongsTo(Customer::class, 'customer_id');
    });

> [!WARNING]  
> 動的リレーションシップを定義するときは、常に明示的なキー名の引数を Eloquent リレーションシップ メソッドに提供します。

<a name="querying-relations"></a>
## 関係のクエリ (Querying Relations)

すべての Eloquent 関係はメソッド経由で定義されるため、実際にクエリを実行して関連モデルをロードしなくても、これらのメソッドを呼び出して関係のインスタンスを取得できます。さらに、すべてのタイプの Eloquent リレーションシップは [クエリビルダ](/docs/{{version}}/queries) としても機能するため、最終的にデータベースに対して SQL クエリを実行する前に、リレーションシップ クエリに制約を連鎖し続けることができます。

たとえば、`User` モデルに多くの関連する `Post` モデルがあるブログ アプリケーションを想像してください。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\HasMany;

    class User extends Model
    {
        /**
         * Get all of the posts for the user.
         */
        public function posts(): HasMany
        {
            return $this->hasMany(Post::class);
        }
    }

次のように、`posts` 関係をクエリし、関係に追加の制約を追加できます。

    use App\Models\User;

    $user = User::find(1);

    $user->posts()->where('active', 1)->get();

リレーションシップでは Laravel [クエリビルダの](/docs/{{version}}/queries) メソッドのいずれかを使用できるため、クエリビルダのドキュメントを参照して、利用可能なすべてのメソッドについて学習してください。

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### リレーションシップ後の `orWhere` 句の連鎖

上の例で示したように、関係をクエリするときに、関係に制約を自由に追加できます。ただし、`orWhere` 句をリレーションシップにチェーンする場合は、`orWhere` 句がリレーションシップ制約と同じレベルで論理的にグループ化されるため、注意してください。

    $user->posts()
            ->where('active', 1)
            ->orWhere('votes', '>=', 100)
            ->get();

上記の例では、次の SQL が生成されます。ご覧のとおり、`or` 句は、100 票を超える投票を含むすべての投稿を返すようにクエリに指示します。クエリは特定のユーザーに制限されなくなりました。

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

ほとんどの状況では、[論理グループ](/docs/{{version}}/queries#logical-grouping) を使用してかっこ内の条件チェックをグループ化する必要があります。

    use Illuminate\Database\Eloquent\Builder;

    $user->posts()
            ->where(function (Builder $query) {
                return $query->where('active', 1)
                             ->orWhere('votes', '>=', 100);
            })
            ->get();

上記の例では、次の SQL が生成されます。論理グループ化により制約が適切にグループ化され、クエリは特定のユーザーに制限されたままであることに注意してください。

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### リレーションシップメソッドと動的プロパティ

Eloquent リレーションシップ クエリに追加の制約を追加する必要がない場合は、プロパティであるかのようにリレーションシップにアクセスできます。たとえば、`User` および `Post` サンプル モデルを引き続き使用すると、次のようにユーザーのすべての投稿にアクセスできます。

    use App\Models\User;

    $user = User::find(1);

    foreach ($user->posts as $post) {
        // ...
    }

動的関係プロパティは「遅延読み込み」を実行します。つまり、実際にアクセスしたときにのみ関係データが読み込まれます。このため、開発者は多くの場合、[熱心な読み込み](#eager-loading) を使用して、モデルのロード後にアクセスされることがわかっている関係を事前にロードします。積極的な読み込みにより、モデルの関係を読み込むために実行する必要がある SQL クエリが大幅に削減されます。

<a name="querying-relationship-existence"></a>
### 関係の存在のクエリ

モデル レコードを取得するとき、関係の存在に基づいて結果を制限したい場合があります。たとえば、少なくとも 1 つのコメントがあるすべてのブログ投稿を取得するとします。これを行うには、関係の名前を `has` メソッドと `orHas` メソッドに渡すことができます。

    use App\Models\Post;

    // Retrieve all posts that have at least one comment...
    $posts = Post::has('comments')->get();

演算子とカウント値を指定して、クエリをさらにカスタマイズすることもできます。

    // Retrieve all posts that have three or more comments...
    $posts = Post::has('comments', '>=', 3)->get();

ネストされた `has` ステートメントは、「ドット」表記を使用して構築できます。たとえば、少なくとも 1 つの画像を含む少なくとも 1 つのコメントを持つすべての投稿を取得できます。

    // Retrieve posts that have at least one comment with images...
    $posts = Post::has('comments.images')->get();

さらに強力な機能が必要な場合は、`whereHas` メソッドと `orWhereHas` メソッドを使用して、コメントの内容を検査するなど、`has` クエリに追加のクエリ制約を定義できます。

    use Illuminate\Database\Eloquent\Builder;

    // Retrieve posts with at least one comment containing words like code%...
    $posts = Post::whereHas('comments', function (Builder $query) {
        $query->where('content', 'like', 'code%');
    })->get();

    // Retrieve posts with at least ten comments containing words like code%...
    $posts = Post::whereHas('comments', function (Builder $query) {
        $query->where('content', 'like', 'code%');
    }, '>=', 10)->get();

> [!WARNING]  
> Eloquent は現在、データベース間の関係の存在に関するクエリをサポートしていません。関係は同じデータベース内に存在する必要があります。

<a name="inline-relationship-existence-queries"></a>
#### インライン関係存在クエリ

関係クエリに関連付けられた単一の単純な where 条件を使用して関係の存在をクエリする場合は、`whereRelation`、`orWhereRelation`、`whereMorphRelation`、および `orWhereMorphRelation` メソッドを使用する方が便利な場合があります。たとえば、未承認のコメントが含まれるすべての投稿をクエリすることができます。

    use App\Models\Post;

    $posts = Post::whereRelation('comments', 'is_approved', false)->get();

もちろん、クエリビルダの `where` メソッドの呼び出しと同様に、演算子を指定することもできます。

    $posts = Post::whereRelation(
        'comments', 'created_at', '>=', now()->subHour()
    )->get();

<a name="querying-relationship-absence"></a>
### 関係の不在のクエリ

モデル レコードを取得するとき、関係がないことに基づいて結果を制限したい場合があります。たとえば、**コメントのない**すべてのブログ投稿を取得するとします。これを行うには、関係の名前を `doesntHave` メソッドと `orDoesntHave` メソッドに渡すことができます。

    use App\Models\Post;

    $posts = Post::doesntHave('comments')->get();

さらに強力な機能が必要な場合は、`whereDoesntHave` メソッドと `orWhereDoesntHave` メソッドを使用して、コメントの内容を検査するなど、追加のクエリ制約を `doesntHave` クエリに追加できます。

    use Illuminate\Database\Eloquent\Builder;

    $posts = Post::whereDoesntHave('comments', function (Builder $query) {
        $query->where('content', 'like', 'code%');
    })->get();

「ドット」表記を使用して、ネストされた関係に対してクエリを実行できます。たとえば、次のクエリはコメントのないすべての投稿を取得します。ただし、禁止されていない作成者からのコメントが含まれる投稿は結果に含まれます。

    use Illuminate\Database\Eloquent\Builder;

    $posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
        $query->where('banned', 0);
    })->get();

<a name="querying-morph-to-relationships"></a>
### 関係へのモーフのクエリ

「モーフ先」関係の存在を照会するには、`whereHasMorph` メソッドと `whereDoesntHaveMorph` メソッドを使用できます。これらのメソッドは、最初の引数として関係の名前を受け入れます。次に、メソッドはクエリに含める関連モデルの名前を受け取ります。最後に、関係クエリをカスタマイズするクロージャを提供できます。

    use App\Models\Comment;
    use App\Models\Post;
    use App\Models\Video;
    use Illuminate\Database\Eloquent\Builder;

    // Retrieve comments associated to posts or videos with a title like code%...
    $comments = Comment::whereHasMorph(
        'commentable',
        [Post::class, Video::class],
        function (Builder $query) {
            $query->where('title', 'like', 'code%');
        }
    )->get();

    // Retrieve comments associated to posts with a title not like code%...
    $comments = Comment::whereDoesntHaveMorph(
        'commentable',
        Post::class,
        function (Builder $query) {
            $query->where('title', 'like', 'code%');
        }
    )->get();

関連する多態性モデルの「タイプ」に基づいてクエリ制約を追加することが必要になる場合があります。 `whereHasMorph` メソッドに渡されるクロージャは、2 番目の引数として `$type` 値を受け取る場合があります。この引数を使用すると、構築されているクエリの「タイプ」を検査できます。

    use Illuminate\Database\Eloquent\Builder;

    $comments = Comment::whereHasMorph(
        'commentable',
        [Post::class, Video::class],
        function (Builder $query, string $type) {
            $column = $type === Post::class ? 'content' : 'title';

            $query->where($column, 'like', 'code%');
        }
    )->get();

<a name="querying-all-morph-to-related-models"></a>
#### すべての関連モデルのクエリ

可能な多態性モデルの配列を渡す代わりに、ワイルドカード値として `*` を指定できます。これにより、Laravel はデータベースから可能なすべての多態性型を取得するように指示されます。 Laravel は、この操作を実行するために追加のクエリを実行します。

    use Illuminate\Database\Eloquent\Builder;

    $comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
        $query->where('title', 'like', 'foo%');
    })->get();

<a name="aggregating-related-models"></a>
## 関連モデルの集約 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 関連モデルのカウント

実際にモデルをロードせずに、特定の関係に関連するモデルの数を数えたい場合があります。これを実現するには、`withCount` メソッドを使用できます。 `withCount` メソッドは、結果のモデルに `{relation}_count` 属性を配置します。

    use App\Models\Post;

    $posts = Post::withCount('comments')->get();

    foreach ($posts as $post) {
        echo $post->comments_count;
    }

配列を `withCount` メソッドに渡すことで、複数のリレーションの「カウント」を追加したり、クエリに追加の制約を追加したりできます。

    use Illuminate\Database\Eloquent\Builder;

    $posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
        $query->where('content', 'like', 'code%');
    }])->get();

    echo $posts[0]->votes_count;
    echo $posts[0]->comments_count;

関係カウントの結果にエイリアスを付けて、同じ関係に対して複数のカウントを許可することもできます。

    use Illuminate\Database\Eloquent\Builder;

    $posts = Post::withCount([
        'comments',
        'comments as pending_comments_count' => function (Builder $query) {
            $query->where('approved', false);
        },
    ])->get();

    echo $posts[0]->comments_count;
    echo $posts[0]->pending_comments_count;

<a name="deferred-count-loading"></a>
#### 遅延カウントのロード

`loadCount` メソッドを使用すると、親モデルがすでに取得された後で関係数をロードできます。

    $book = Book::first();

    $book->loadCount('genres');

カウント クエリに追加のクエリ制約を設定する必要がある場合は、カウントしたい関係をキーとする配列を渡すことができます。配列値は、クエリビルダ インスタンスを受け取るクロージャである必要があります。

    $book->loadCount(['reviews' => function (Builder $query) {
        $query->where('rating', 5);
    }])

<a name="relationship-counting-and-custom-select-statements"></a>
#### 関係カウントとカスタム選択ステートメント

`withCount` を `select` ステートメントと組み合わせている場合は、必ず `select` メソッドの後に `withCount` を呼び出してください。

    $posts = Post::select(['title', 'body'])
                    ->withCount('comments')
                    ->get();

<a name="other-aggregate-functions"></a>
### その他の集計関数

`withCount` メソッドに加えて、Eloquent は `withMin`、`withMax`、`withAvg`、`withSum`、および `withExists` メソッドを提供します。これらのメソッドは、結果のモデルに `{relation}_{function}_{column}` 属性を配置します。

    use App\Models\Post;

    $posts = Post::withSum('comments', 'votes')->get();

    foreach ($posts as $post) {
        echo $post->comments_sum_votes;
    }

別の名前を使用して集計関数の結果にアクセスしたい場合は、独自のエイリアスを指定できます。

    $posts = Post::withSum('comments as total_comments', 'votes')->get();

    foreach ($posts as $post) {
        echo $post->total_comments;
    }

`loadCount` メソッドと同様に、これらのメソッドの遅延バージョンも使用できます。これらの追加の集計操作は、すでに取得されている Eloquent モデルに対して実行できます。

    $post = Post::first();

    $post->loadSum('comments', 'votes');

これらの集計メソッドを `select` ステートメントと組み合わせている場合は、必ず `select` メソッドの後に集計メソッドを呼び出してください。

    $posts = Post::select(['title', 'body'])
                    ->withExists('comments')
                    ->get();

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To Relationship で関連モデルをカウントする

「モーフ」関係、およびその関係によって返されるさまざまなエンティティの関連モデル数を一括ロードしたい場合は、`with` メソッドを `morphTo` 関係の `morphWithCount` メソッドと組み合わせて利用できます。

この例では、`Photo` モデルと `Post` モデルが `ActivityFeed` モデルを作成すると仮定します。 `ActivityFeed` モデルは、特定の `ActivityFeed` インスタンスの親 `Photo` または `Post` モデルを取得できる `parentable` という名前の「モーフ」関係を定義していると仮定します。さらに、`Photo` モデルには `Tag` モデルが「多数」あり、`Post` モデルには `Comment` モデルが「多数」あると仮定します。

ここで、`ActivityFeed` インスタンスを取得し、各 `ActivityFeed` インスタンスの `parentable` 親モデルを一括ロードするとします。さらに、各親写真に関連付けられているタグの数と、各親投稿に関連付けられているコメントの数を取得したいと考えています。

    use Illuminate\Database\Eloquent\Relations\MorphTo;

    $activities = ActivityFeed::with([
        'parentable' => function (MorphTo $morphTo) {
            $morphTo->morphWithCount([
                Photo::class => ['tags'],
                Post::class => ['comments'],
            ]);
        }])->get();

<a name="morph-to-deferred-count-loading"></a>
#### 遅延カウントのロード

すでに `ActivityFeed` モデルのセットを取得しており、アクティビティ フィードに関連付けられたさまざまな `parentable` モデルのネストされた関係数をロードしたいとします。これを実現するには、`loadMorphCount` メソッドを使用できます。

    $activities = ActivityFeed::with('parentable')->get();

    $activities->loadMorphCount('parentable', [
        Photo::class => ['tags'],
        Post::class => ['comments'],
    ]);

<a name="eager-loading"></a>
## 熱心な読み込み (Eager Loading)

Eloquent 関係にプロパティとしてアクセスすると、関連モデルは「遅延読み込み」されます。これは、最初にプロパティにアクセスするまで、リレーションシップ データが実際には読み込まれないことを意味します。ただし、Eloquent は、親モデルをクエリするときに関係を「熱心にロード」できます。積極的な読み込みにより、「N + 1」クエリの問題が軽減されます。 N + 1 クエリの問題を説明するために、`Author` モデルに「属する」 `Book` モデルを考えてみましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsTo;

    class Book extends Model
    {
        /**
         * Get the author that wrote the book.
         */
        public function author(): BelongsTo
        {
            return $this->belongsTo(Author::class);
        }
    }

次に、すべての書籍とその著者を取得しましょう。

    use App\Models\Book;

    $books = Book::all();

    foreach ($books as $book) {
        echo $book->author->name;
    }

このループは、データベース テーブル内のすべての書籍を取得するために 1 つのクエリを実行し、次に書籍ごとに別のクエリを実行して書籍の著者を取得します。したがって、書籍が 25 冊ある場合、上記のコードは 26 のクエリを実行します。1 つは元の書籍に対して 1 クエリで、各書籍の著者を取得するために 25 の追加クエリが実行されます。

ありがたいことに、積極的な読み込みを使用すると、この操作を 2 つのクエリのみに減らすことができます。クエリを構築するとき、`with` メソッドを使用して、どのリレーションシップを積極的にロードする必要があるかを指定できます。

    $books = Book::with('author')->get();

    foreach ($books as $book) {
        echo $book->author->name;
    }

この操作では、2 つのクエリのみが実行されます。1 つはすべての書籍を取得するクエリ、もう 1 つはすべての書籍のすべての著者を取得するクエリです。

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 複数の関係を熱心にロードする

場合によっては、複数の異なる関係を積極的にロードする必要があるかもしれません。これを行うには、関係の配列を `with` メソッドに渡すだけです。

    $books = Book::with(['author', 'publisher'])->get();

<a name="nested-eager-loading"></a>
#### ネストされた熱心な読み込み

関係の関係を積極的にロードするには、「ドット」構文を使用できます。たとえば、本の著者すべてと著者の個人的な連絡先すべてを熱心にロードしてみましょう。

    $books = Book::with('author.contacts')->get();

あるいは、ネストされた配列を `with` メソッドに提供することで、ネストされた一括ロードされた関係を指定することもできます。これは、複数のネストされた関係を一括ロードするときに便利です。

    $books = Book::with([
        'author' => [
            'contacts',
            'publisher',
        ],
    ])->get();

<a name="nested-eager-loading-morphto-relationships"></a>
#### ネストされた熱心なロード `morphTo` 関係

`morphTo` 関係、およびその関係によって返されるさまざまなエンティティのネストされた関係を一括ロードしたい場合は、`with` メソッドを `morphTo` 関係の `morphWith` メソッドと組み合わせて使用​​できます。この方法を説明するために、次のモデルを考えてみましょう。

    <?php

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphTo;

    class ActivityFeed extends Model
    {
        /**
         * Get the parent of the activity feed record.
         */
        public function parentable(): MorphTo
        {
            return $this->morphTo();
        }
    }

この例では、`Event`、`Photo`、および `Post` モデルが `ActivityFeed` モデルを作成すると仮定します。さらに、`Event` モデルは `Calendar` モデルに属し、`Photo` モデルは `Tag` モデルに関連付けられ、`Post` モデルは `Author` モデルに属すると仮定します。

これらのモデル定義と関係を使用して、`ActivityFeed` モデル インスタンスを取得し、すべての `parentable` モデルとそれぞれのネストされた関係を一括ロードできます。

    use Illuminate\Database\Eloquent\Relations\MorphTo;

    $activities = ActivityFeed::query()
        ->with(['parentable' => function (MorphTo $morphTo) {
            $morphTo->morphWith([
                Event::class => ['calendar'],
                Photo::class => ['tags'],
                Post::class => ['author'],
            ]);
        }])->get();

<a name="eager-loading-specific-columns"></a>
#### 特定の列を積極的にロードする

取得するリレーションシップのすべての列が必ずしも必要であるとは限りません。このため、Eloquent では、関係のどの列を取得するかを指定できます。

    $books = Book::with('author:id,name,book_id')->get();

> [!WARNING]  
> この機能を使用する場合は、取得する列のリストに `id` 列と関連する外部キー列を常に含める必要があります。

<a name="eager-loading-by-default"></a>
#### デフォルトでの積極的なロード

場合によっては、モデルを取得するときに常にいくつかの関係をロードしたい場合があります。これを実現するには、モデルに `$with` プロパティを定義します。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsTo;

    class Book extends Model
    {
        /**
         * The relationships that should always be loaded.
         *
         * @var array
         */
        protected $with = ['author'];

        /**
         * Get the author that wrote the book.
         */
        public function author(): BelongsTo
        {
            return $this->belongsTo(Author::class);
        }

        /**
         * Get the genre of the book.
         */
        public function genre(): BelongsTo
        {
            return $this->belongsTo(Genre::class);
        }
    }

単一のクエリの `$with` プロパティから項目を削除したい場合は、`without` メソッドを使用できます。

    $books = Book::without('author')->get();

単一のクエリの `$with` プロパティ内のすべての項目をオーバーライドする場合は、`withOnly` メソッドを使用できます。

    $books = Book::withOnly('genre')->get();

<a name="constraining-eager-loads"></a>
### 熱心なロードの制限

場合によっては、リレーションシップを一括読み込みしたいときに、一括読み込みクエリに追加のクエリ条件を指定することもできます。これを実現するには、関係の配列を `with` メソッドに渡します。ここで、配列のキーは関係名、配列の値は、熱心な読み込みクエリに追加の制約を追加するクロージャです。

    use App\Models\User;
    use Illuminate\Contracts\Database\Eloquent\Builder;

    $users = User::with(['posts' => function (Builder $query) {
        $query->where('title', 'like', '%code%');
    }])->get();

この例では、Eloquent は、投稿の `title` 列に `code` という単語が含まれる投稿のみを一括読み込みします。他の [クエリビルダ](/docs/{{version}}/queries) メソッドを呼び出して、積極的な読み込み操作をさらにカスタマイズすることもできます。

    $users = User::with(['posts' => function (Builder $query) {
        $query->orderBy('created_at', 'desc');
    }])->get();

> [!WARNING]  
> `limit` および `take` クエリビルダ メソッドは、熱心な読み込みを制約する場合には使用できない場合があります。

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 関係の積極的なロードの制約

`morphTo` 関係を積極的にロードしている場合、Eloquent は複数のクエリを実行して、各タイプの関連モデルを取得します。 `MorphTo` リレーションの `constrain` メソッドを使用して、これらのクエリのそれぞれに追加の制約を追加できます。

    use Illuminate\Database\Eloquent\Relations\MorphTo;

    $comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
        $morphTo->constrain([
            Post::class => function ($query) {
                $query->whereNull('hidden_at');
            },
            Video::class => function ($query) {
                $query->where('type', 'educational');
            },
        ]);
    }])->get();

この例では、Eloquent は、非表示になっていない投稿と、`type` 値が「教育」であるビデオのみを積極的に読み込みます。

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 関係の存在による熱心な負荷の抑制

同じ条件に基づいて関係を読み込むと同時に、関係の存在を確認する必要がある場合があります。たとえば、指定されたクエリ条件に一致する子 `Post` モデルを持つ `User` モデルのみを取得し、一致する投稿を一括読み込みすることもできます。これは、`withWhereHas` メソッドを使用して実行できます。

    use App\Models\User;

    $users = User::withWhereHas('posts', function ($query) {
        $query->where('featured', true);
    })->get();

<a name="lazy-eager-loading"></a>
### 遅延熱心な読み込み

場合によっては、親モデルがすでに取得された後でリレーションシップを積極的にロードする必要がある場合があります。たとえば、これは、関連モデルをロードするかどうかを動的に決定する必要がある場合に便利です。

    use App\Models\Book;

    $books = Book::all();

    if ($someCondition) {
        $books->load('author', 'publisher');
    }

熱心な読み込みクエリに追加のクエリ制約を設定する必要がある場合は、読み込みたい関係をキーとする配列を渡すことができます。配列値は、クエリ インスタンスを受け取るクロージャ インスタンスである必要があります。

    $author->load(['books' => function (Builder $query) {
        $query->orderBy('published_date', 'asc');
    }]);

関係がまだロードされていない場合にのみ関係をロードするには、`loadMissing` メソッドを使用します。

    $book->loadMissing('author');

<a name="nested-lazy-eager-loading-morphto"></a>
#### ネストされた Lazy Eager Loading と `morphTo`

`morphTo` 関係、およびその関係によって返される可能性のあるさまざまなエンティティのネストされた関係を一括ロードしたい場合は、`loadMorph` メソッドを使用できます。

このメソッドは、最初の引数として `morphTo` 関係の名前を受け入れ、2 番目の引数としてモデルと関係のペアの配列を受け入れます。この方法を説明するために、次のモデルを考えてみましょう。

    <?php

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\MorphTo;

    class ActivityFeed extends Model
    {
        /**
         * Get the parent of the activity feed record.
         */
        public function parentable(): MorphTo
        {
            return $this->morphTo();
        }
    }

この例では、`Event`、`Photo`、および `Post` モデルが `ActivityFeed` モデルを作成すると仮定します。さらに、`Event` モデルは `Calendar` モデルに属し、`Photo` モデルは `Tag` モデルに関連付けられ、`Post` モデルは `Author` モデルに属すると仮定します。

これらのモデル定義と関係を使用して、`ActivityFeed` モデル インスタンスを取得し、すべての `parentable` モデルとそれぞれのネストされた関係を一括ロードできます。

    $activities = ActivityFeed::with('parentable')
        ->get()
        ->loadMorph('parentable', [
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);

<a name="preventing-lazy-loading"></a>
### 遅延読み込みの防止

前述したように、積極的な読み込み関係により、多くの場合、アプリケーションに大幅なパフォーマンス上の利点がもたらされます。したがって、必要に応じて、リレーションシップの遅延読み込みを常に防止するように Laravel に指示することもできます。これを実現するには、基本 Eloquent モデル クラスによって提供される `preventLazyLoading` メソッドを呼び出すことができます。通常、このメソッドはアプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で呼び出す必要があります。

`preventLazyLoading` メソッドは、遅延読み込みを防止する必要があるかどうかを示すオプションのブール引数を受け入れます。たとえば、非実稼働環境でのみ遅延ロードを無効にして、実稼働コードに遅延ロード関係が誤って存在した場合でも実稼働環境が正常に機能し続けるようにすることができます。

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

遅延ロードを防止した後、アプリケーションが Eloquent 関係を遅延ロードしようとすると、Eloquent は `Illuminate\Database\LazyLoadingViolationException` 例外をスローします。

`handleLazyLoadingViolationsUsing` メソッドを使用して、遅延読み込み違反の動作をカスタマイズできます。たとえば、このメソッドを使用すると、例外を発生させてアプリケーションの実行を中断するのではなく、遅延読み込み違反のみをログに記録するように指示できます。

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 関連モデルの挿入と更新 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### `save` メソッド

Eloquent は、関係に新しいモデルを追加するための便利な方法を提供します。たとえば、投稿に新しいコメントを追加する必要がある場合があります。 `Comment` モデルの `post_id` 属性を手動で設定する代わりに、リレーションシップの `save` メソッドを使用してコメントを挿入できます。

    use App\Models\Comment;
    use App\Models\Post;

    $comment = new Comment(['message' => 'A new comment.']);

    $post = Post::find(1);

    $post->comments()->save($comment);

`comments` 関係に動的プロパティとしてアクセスしていないことに注意してください。代わりに、`comments` メソッドを呼び出して関係のインスタンスを取得しました。 `save` メソッドは、適切な `post_id` 値を新しい `Comment` モデルに自動的に追加します。

複数の関連モデルを保存する必要がある場合は、`saveMany` メソッドを使用できます。

    $post = Post::find(1);

    $post->comments()->saveMany([
        new Comment(['message' => 'A new comment.']),
        new Comment(['message' => 'Another new comment.']),
    ]);

`save` メソッドと `saveMany` メソッドは、指定されたモデル インスタンスを永続化しますが、親モデルに既にロードされているメモリ内の関係に、新しく永続化されたモデルを追加しません。 `save` メソッドまたは `saveMany` メソッドを使用した後にリレーションシップにアクセスする予定がある場合は、`refresh` メソッドを使用してモデルとそのリレーションシップをリロードすることをお勧めします。

    $post->comments()->save($comment);

    $post->refresh();

    // All comments, including the newly saved comment...
    $post->comments;

<a name="the-push-method"></a>
#### モデルと関係を再帰的に保存する

モデルとそのすべての関連関係を `save` したい場合は、`push` メソッドを使用できます。この例では、`Post` モデルとそのコメント、およびコメントの作成者が保存されます。

    $post = Post::find(1);

    $post->comments[0]->message = 'Message';
    $post->comments[0]->author->name = 'Author Name';

    $post->push();

`pushQuietly` メソッドは、イベントを発生させずにモデルとその関連関係を保存するために使用できます。

    $post->pushQuietly();

<a name="the-create-method"></a>
### `create` メソッド

`save` メソッドと `saveMany` メソッドに加えて、属性の配列を受け取り、モデルを作成してデータベースに挿入する `create` メソッドも使用できます。 `save` と `create` の違いは、`save` は完全な Eloquent モデル インスタンスを受け入れるのに対し、`create` はプレーンな PHP `array` を受け入れることです。新しく作成されたモデルは、`create` メソッドによって返されます。

    use App\Models\Post;

    $post = Post::find(1);

    $comment = $post->comments()->create([
        'message' => 'A new comment.',
    ]);

`createMany` メソッドを使用して、複数の関連モデルを作成できます。

    $post = Post::find(1);

    $post->comments()->createMany([
        ['message' => 'A new comment.'],
        ['message' => 'Another new comment.'],
    ]);

`createQuietly` メソッドと `createManyQuietly` メソッドは、イベントをディスパッチせずにモデルを作成するために使用できます。

    $user = User::find(1);

    $user->posts()->createQuietly([
        'title' => 'Post title.',
    ]);
    
    $user->posts()->createManyQuietly([
        ['title' => 'First post.'],
        ['title' => 'Second post.'],
    ]);

`findOrNew`、`firstOrNew`、`firstOrCreate`、および `updateOrCreate` メソッドを [関係に関するモデルを作成および更新する](/docs/{{version}}/eloquent#upserts) に使用することもできます。

> [!NOTE]  
> `create` メソッドを使用する前に、必ず [一括割り当て](/docs/{{version}}/eloquent#mass-assignment) ドキュメントを確認してください。

<a name="updating-belongs-to-relationships"></a>
### 関係に属します

子モデルを新しい親モデルに割り当てたい場合は、`associate` メソッドを使用できます。この例では、`User` モデルは、`Account` モデルに対する `belongsTo` 関係を定義します。この `associate` メソッドは、子モデルに外部キーを設定します。

    use App\Models\Account;

    $account = Account::find(10);

    $user->account()->associate($account);

    $user->save();

子モデルから親モデルを削除するには、`dissociate` メソッドを使用できます。このメソッドは、リレーションシップの外部キーを `null` に設定します。

    $user->account()->dissociate();

    $user->save();

<a name="updating-many-to-many-relationships"></a>
### 多対多の関係

<a name="attaching-detaching"></a>
#### 取り付け・取り外し

Eloquent は、多対多の関係の操作をより便利にするメソッドも提供します。たとえば、1 人のユーザーが多数のロールを持つことができ、1 つのロールが多数のユーザーを持つことができると考えてみましょう。 `attach` メソッドを使用して、関係の中間テーブルにレコードを挿入することでユーザーにロールをアタッチできます。

    use App\Models\User;

    $user = User::find(1);

    $user->roles()->attach($roleId);

リレーションシップをモデルにアタッチするときに、中間テーブルに挿入する追加データの配列を渡すこともできます。

    $user->roles()->attach($roleId, ['expires' => $expires]);

場合によっては、ユーザーから役割を削除することが必要になる場合があります。多対多の関係レコードを削除するには、`detach` メソッドを使用します。 `detach` メソッドは、中間テーブルから適切なレコードを削除します。ただし、両方のモデルがデータベースに残ります。

    // Detach a single role from the user...
    $user->roles()->detach($roleId);

    // Detach all roles from the user...
    $user->roles()->detach();

便宜上、`attach` と `detach` は入力として ID の配列も受け入れます。

    $user = User::find(1);

    $user->roles()->detach([1, 2, 3]);

    $user->roles()->attach([
        1 => ['expires' => $expires],
        2 => ['expires' => $expires],
    ]);

<a name="syncing-associations"></a>
#### 関連付けの同期

`sync` メソッドを使用して多対多の関連付けを構築することもできます。 `sync` メソッドは、中間テーブルに配置する ID の配列を受け入れます。指定された配列にない ID は中間テーブルから削除されます。したがって、この操作が完了すると、指定された配列内の ID のみが中間テーブルに存在します。

    $user->roles()->sync([1, 2, 3]);

追加の中間テーブル値を ID とともに渡すこともできます。

    $user->roles()->sync([1 => ['expires' => true], 2, 3]);

同期されたモデル ID のそれぞれに同じ中間テーブル値を挿入したい場合は、`syncWithPivotValues` メソッドを使用できます。

    $user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);

指定された配列から欠落している既存の ID を切り離したくない場合は、`syncWithoutDetaching` メソッドを使用できます。

    $user->roles()->syncWithoutDetaching([1, 2, 3]);

<a name="toggling-associations"></a>
#### 関連付けの切り替え

多対多の関係では、指定された関連モデル ID の接続ステータスを「切り替える」`toggle` メソッドも提供されます。指定された ID が現在アタッチされている場合は、デタッチされます。同様に、現在デタッチされている場合は、アタッチされます。

    $user->roles()->toggle([1, 2, 3]);

追加の中間テーブル値を ID とともに渡すこともできます。

    $user->roles()->toggle([
        1 => ['expires' => true],
        2 => ['expires' => true],
    ]);

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 中間テーブルのレコードの更新

リレーションシップの中間テーブル内の既存の行を更新する必要がある場合は、`updateExistingPivot` メソッドを使用できます。このメソッドは、中間レコードの外部キーと更新する属性の配列を受け取ります。

    $user = User::find(1);

    $user->roles()->updateExistingPivot($roleId, [
        'active' => false,
    ]);

<a name="touching-parent-timestamps"></a>
## 親のタイムスタンプに触れる (Touching Parent Timestamps)

モデルが、`Post` に属する `Comment` など、別のモデルとの `belongsTo` または `belongsToMany` 関係を定義する場合、子モデルが更新されるときに親のタイムスタンプを更新すると役立つ場合があります。

たとえば、`Comment` モデルが更新されるとき、所有する `Post` の `updated_at` タイムスタンプを自動的に「タッチ」して、現在の日付と時刻に設定することができます。これを実現するには、子モデルの更新時に `updated_at` タイムスタンプを更新する必要があるリレーションシップの名前を含む `touches` プロパティを子モデルに追加します。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsTo;

    class Comment extends Model
    {
        /**
         * All of the relationships to be touched.
         *
         * @var array
         */
        protected $touches = ['post'];

        /**
         * Get the post that the comment belongs to.
         */
        public function post(): BelongsTo
        {
            return $this->belongsTo(Post::class);
        }
    }

> [!WARNING]  
> 親モデルのタイムスタンプは、Eloquent の `save` メソッドを使用して子モデルが更新された場合にのみ更新されます。

