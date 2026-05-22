# Eloquent: 工場 (Eloquent: Factories)

- [Introduction](#introduction)
- [モデルファクトリーの定義](#defining-model-factories)
    - [工場の生成](#generating-factories)
    - [工場出荷時の状態](#factory-states)
    - [ファクトリーコールバック](#factory-callbacks)
- [ファクトリを使用したモデルの作成](#creating-models-using-factories)
    - [モデルのインスタンス化](#instantiating-models)
    - [永続的なモデル](#persisting-models)
    - [Sequences](#sequences)
- [工場との関係](#factory-relationships)
    - [多くの関係がある](#has-many-relationships)
    - [関係に属します](#belongs-to-relationships)
    - [多対多の関係](#many-to-many-relationships)
    - [ポリモーフィックな関係](#polymorphic-relationships)
    - [ファクトリ内の関係の定義](#defining-relationships-within-factories)
    - [既存の関係モデルのリサイクル](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 導入 (Introduction)

アプリケーションをテストするとき、またはデータベースをシードするとき、データベースにいくつかのレコードを挿入する必要がある場合があります。各列の値を手動で指定する代わりに、Laravel では、モデルファクトリーを使用して、[Eloquent モデル](/docs/{{version}}/eloquent) ごとにデフォルト属性のセットを定義できます。

ファクトリの作成方法の例を確認するには、アプリケーション内の `database/factories/UserFactory.php` ファイルを見てください。このファクトリはすべての新しい Laravel アプリケーションに含まれており、次のファクトリ定義が含まれています。

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

ご覧のとおり、最も基本的な形式では、ファクトリは Laravel の基本ファクトリ クラスを拡張し、`definition` メソッドを定義するクラスです。 `definition` メソッドは、ファクトリを使用してモデルを作成するときに適用する必要がある属性値のデフォルトのセットを返します。

`fake` ヘルパを介して、ファクトリは [Faker](https://github.com/FakerPHP/Faker) PHP ライブラリにアクセスできるため、テストやシード用にさまざまな種類のランダム データを簡単に生成できます。

> [!NOTE]
> `config/app.php` 構成ファイルの `faker_locale` オプションを更新することで、アプリケーションの Faker ロケールを変更できます。

<a name="defining-model-factories"></a>
## モデルファクトリーの定義 (Defining Model Factories)

<a name="generating-factories"></a>
### 工場の生成

ファクトリを作成するには、`make:factory` [Artisan コマンド](/docs/{{version}}/artisan) を実行します。

```shell
php artisan make:factory PostFactory
```

新しいファクトリ クラスは、`database/factories` ディレクトリに配置されます。

<a name="factory-and-model-discovery-conventions"></a>
#### モデルとファクトリーの検出規則

ファクトリを定義したら、`Illuminate\Database\Eloquent\Factories\HasFactory` トレイトによってモデルに提供される静的 `factory` メソッドを使用して、そのモデルのファクトリ インスタンスをインスタンス化できます。

`HasFactory` トレイトの `factory` メソッドは、規約を使用して、トレイトが割り当てられているモデルに適切なファクトリを決定します。具体的には、このメソッドは、モデル名と一致するクラス名を持ち、接尾辞が `Factory` である `Database\Factories` 名前空間内のファクトリを検索します。これらの規則が特定のアプリケーションまたはファクトリに適用されない場合は、`UseFactory` 属性をモデルに追加して、モデルのファクトリを手動で指定できます。

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

あるいは、モデルの `newFactory` メソッドを上書きして、モデルの対応するファクトリのインスタンスを直接返すこともできます。

```php
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

次に、対応するファクトリで `model` プロパティを定義します。

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 工場出荷時の状態

状態操作メソッドを使用すると、モデル ファクトリに任意の組み合わせで適用できる個別の変更を定義できます。たとえば、`Database\Factories\UserFactory` ファクトリには、デフォルトの属性値の 1 つを変更する `suspended` 状態メソッドが含まれる場合があります。

状態変換メソッドは通常、Laravel の基本ファクトリ クラスによって提供される `state` メソッドを呼び出します。 `state` メソッドは、ファクトリに定義された生の属性の配列を受け取るクロージャーを受け入れ、変更する属性の配列を返す必要があります。

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a name="trashed-state"></a>
#### 「ゴミ箱」状態

Eloquent モデルが [ソフト削除されました](/docs/{{version}}/eloquent#soft-deleting) である可能性がある場合は、組み込みの `trashed` 状態メソッドを呼び出して、作成されたモデルがすでに「論理的に削除」されている必要があることを示すことができます。 `trashed` 状態はすべてのファクトリで自動的に使用できるため、手動で定義する必要はありません。

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### ファクトリーコールバック

ファクトリ コールバックは、`afterMaking` メソッドと `afterCreating` メソッドを使用して登録され、モデルの作成後に追加のタスクを実行できるようになります。ファクトリ クラスで `configure` メソッドを定義して、これらのコールバックを登録する必要があります。このメソッドは、ファクトリがインスタンス化されるときに Laravel によって自動的に呼び出されます。

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // ...
        })->afterCreating(function (User $user) {
            // ...
        });
    }

    // ...
}
```

状態メソッド内にファクトリ コールバックを登録して、特定の状態に固有の追加タスクを実行することもできます。

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // ...
    })->afterCreating(function (User $user) {
        // ...
    });
}
```

<a name="creating-models-using-factories"></a>
## ファクトリを使用したモデルの作成 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### モデルのインスタンス化

ファクトリを定義したら、`Illuminate\Database\Eloquent\Factories\HasFactory` トレイトによってモデルに提供される静的 `factory` メソッドを使用して、そのモデルのファクトリ インスタンスをインスタンス化できます。モデル作成の例をいくつか見てみましょう。まず、`make` メソッドを使用して、モデルをデータベースに保存せずに作成します。

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` メソッドを使用して、多くのモデルのコレクションを作成できます。

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 状態の適用

[states](#factory-states) のいずれかをモデルに適用することもできます。複数の状態変換をモデルに適用したい場合は、状態変換メソッドを直接呼び出すだけです。

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 属性の上書き

モデルのデフォルト値の一部をオーバーライドしたい場合は、値の配列を `make` メソッドに渡すことができます。指定された属性のみが置換され、残りの属性は工場で指定されたデフォルト値に設定されたままになります。

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

あるいは、`state` メソッドをファクトリ インスタンスで直接呼び出して、インライン状態変換を実行することもできます。

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> ファクトリを使用してモデルを作成する場合、[一括割り当ての保護](/docs/{{version}}/eloquent#mass-assignment) は自動的に無効になります。

<a name="persisting-models"></a>
### 永続的なモデル

`create` メソッドはモデル インスタンスをインスタンス化し、Eloquent の `save` メソッドを使用してデータベースに永続化します。

```php
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```

属性の配列を `create` メソッドに渡すことで、ファクトリのデフォルトのモデル属性をオーバーライドできます。

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### シーケンス

場合によっては、作成されたモデルごとに特定のモデル属性の値を変更したい場合があります。これは、状態変換をシーケンスとして定義することで実現できます。たとえば、作成されたユーザーごとに、`admin` 列の値を `Y` と `N` の間で切り替えることができます。

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        ['admin' => 'Y'],
        ['admin' => 'N'],
    ))
    ->create();
```

この例では、`admin` 値 `Y` で 5 人のユーザーが作成され、`admin` 値 `N` で 5 人のユーザーが作成されます。

必要に応じて、シーケンス値としてクロージャを含めることができます。クロージャは、シーケンスに新しい値が必要になるたびに呼び出されます。

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

シーケンス クロージャ内では、クロージャに挿入されるシーケンス インスタンスの `$index` プロパティにアクセスできます。 `$index` プロパティには、これまでに発生したシーケンスの反復回数が含まれます。

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

便宜上、`sequence` メソッドを使用してシーケンスを適用することもできます。これは単に `state` メソッドを内部で呼び出すだけです。 `sequence` メソッドは、クロージャまたはシーケンスされた属性の配列を受け入れます。

```php
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```

<a name="factory-relationships"></a>
## 工場との関係 (Factory Relationships)

<a name="has-many-relationships"></a>
### 多くの関係がある

次に、Laravel の Fluent Factory メソッドを使用して Eloquent モデルの関係を構築してみましょう。まず、アプリケーションに `App\Models\User` モデルと `App\Models\Post` モデルがあると仮定します。また、`User` モデルが `Post` との `hasMany` 関係を定義すると仮定します。 Laravel のファクトリーが提供する `has` メソッドを使用して、3 つの投稿を持つユーザーを作成できます。 `has` メソッドはファクトリ インスタンスを受け入れます。

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

慣例により、`Post` モデルを `has` メソッドに渡すとき、Laravel は、`User` モデルには関係を定義する `posts` メソッドが必要であると想定します。必要に応じて、操作する関係の名前を明示的に指定できます。

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

もちろん、関連するモデルに対して状態操作を実行することもできます。さらに、状態変更で親モデルへのアクセスが必要な場合は、クロージャーベースの状態変換を渡すことができます。

```php
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
    )
    ->create();
```

<a name="has-many-relationships-using-magic-methods"></a>
#### 魔法の方法を使用する

便宜上、Laravel のマジックファクトリー関係メソッドを使用して関係を構築できます。たとえば、次の例では、規則を使用して、`User` モデルの `posts` リレーションシップ メソッドを介して関連モデルを作成する必要があることを決定します。

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

マジック メソッドを使用してファクトリ リレーションシップを作成する場合、関連モデルをオーバーライドする属性の配列を渡すことができます。

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

状態変更で親モデルへのアクセスが必要な場合は、クロージャベースの状態変換を提供できます。

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### 関係に属します

ファクトリを使用して「has many」関係を構築する方法を説明したので、その逆の関係を見てみましょう。 `for` メソッドは、工場で作成されたモデルが属する親モデルを定義するために使用できます。たとえば、1 人のユーザーに属する 3 つの `App\Models\Post` モデル インスタンスを作成できます。

```php
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```

作成中のモデルに関連付ける親モデル インスタンスがすでにある場合は、そのモデル インスタンスを `for` メソッドに渡すことができます。

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 魔法の方法を使用する

便宜上、Laravel のマジックファクトリー関係メソッドを使用して、「所属する」関係を定義できます。たとえば、次の例では、規則を使用して、3 つの投稿が `Post` モデルの `user` 関係に属する必要があることを決定します。

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### 多対多の関係

[多くの関係がある](#has-many-relationships) と同様に、「多対多」関係は `has` メソッドを使用して作成できます。

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### ピボットテーブルの属性

モデルをリンクするピボット/中間テーブルに設定する必要がある属性を定義する必要がある場合は、`hasAttached` メソッドを使用できます。このメソッドは、ピボット テーブルの属性名と値の配列を 2 番目の引数として受け入れます。

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```

状態変更に関連モデルへのアクセスが必要な場合は、クロージャベースの状態変換を提供できます。

```php
$user = User::factory()
    ->hasAttached(
        Role::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['name' => $user->name.' Role'];
            }),
        ['active' => true]
    )
    ->create();
```

作成中のモデルにアタッチしたいモデル インスタンスが既にある場合は、そのモデル インスタンスを `hasAttached` メソッドに渡すことができます。この例では、同じ 3 つのロールが 3 人のユーザー全員にアタッチされます。

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 魔法の方法を使用する

便宜上、Laravel のマジックファクトリー関係メソッドを使用して多対多の関係を定義できます。たとえば、次の例では、規則を使用して、`User` モデルの `roles` リレーションシップ メソッドを介して関連モデルを作成する必要があることを決定します。

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### ポリモーフィックな関係

[ポリモーフィックな関係](/docs/{{version}}/eloquent-relationships#polymorphic-relationships) は、ファクトリを使用して作成することもできます。ポリモーフィックな「モーフ・メニー」リレーションシップは、典型的な「ハズ・メニー」リレーションシップと同じ方法で作成されます。たとえば、`App\Models\Post` モデルに `App\Models\Comment` モデルとの `morphMany` 関係がある場合、次のようになります。

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### 関係へのモーフ

`morphTo` 関係の作成にマジック メソッドを使用することはできません。代わりに、`for` メソッドを直接使用し、関係の名前を明示的に指定する必要があります。たとえば、`Comment` モデルに、`morphTo` 関係を定義する `commentable` メソッドがあると想像してください。この状況では、`for` メソッドを直接使用して、1 つの投稿に属する 3 つのコメントを作成できます。

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### ポリモーフィックな多対多の関係

ポリモーフィックな「多対多」(`morphToMany` / `morphedByMany`) 関係は、非ポリモーフィックな「多対多」関係と同様に作成できます。

```php
use App\Models\Tag;
use App\Models\Video;

$video = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

もちろん、魔法の `has` メソッドを使用して、多態性の「多対多」関係を作成することもできます。

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### ファクトリ内の関係の定義

モデル ファクトリ内でリレーションシップを定義するには、通常、リレーションシップの外部キーに新しいファクトリ インスタンスを割り当てます。これは通常、`belongsTo` 関係や `morphTo` 関係などの「逆」関係に対して行われます。たとえば、投稿の作成時に新しいユーザーを作成したい場合は、次の手順を実行します。

```php
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

リレーションシップの列がそれを定義するファクトリに依存する場合は、属性にクロージャを割り当てることができます。クロージャはファクトリの評価された属性配列を受け取ります。

```php
/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a name="recycling-an-existing-model-for-relationships"></a>
### 既存の関係モデルのリサイクル

別のモデルと共通の関係を共有するモデルがある場合は、`recycle` メソッドを使用して、関連モデルの単一インスタンスがファクトリによって作成されたすべての関係に対して確実にリサイクルされるようにすることができます。

たとえば、`Airline`、`Flight`、および `Ticket` モデルがあり、チケットが航空会社とフライトに属し、フライトも航空会社に属しているとします。チケットを作成するときは、おそらくチケットとフライトの両方に同じ航空会社が必要になるため、航空会社インスタンスを `recycle` メソッドに渡すことができます。

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` メソッドは、共通のユーザーまたはチームに属するモデルがある場合に特に便利です。

`recycle` メソッドは、既存のモデルのコレクションも受け入れます。コレクションが `recycle` メソッドに提供されると、ファクトリがそのタイプのモデルを必要とするときに、コレクションからランダムなモデルが選択されます。

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```

