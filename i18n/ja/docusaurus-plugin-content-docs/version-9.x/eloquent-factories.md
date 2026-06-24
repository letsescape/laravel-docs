<!-- # Eloquent: Factories -->
# Eloquent: Factories

- [Introduction](#introduction)
- [Defining Model Factories](#defining-model-factories)
    - [Generating Factories](#generating-factories)
    - [Factory States](#factory-states)
    - [Factory Callbacks](#factory-callbacks)
- [Creating Models Using Factories](#creating-models-using-factories)
    - [Instantiating Models](#instantiating-models)
    - [Persisting Models](#persisting-models)
    - [Sequences](#sequences)
- [Factory Relationships](#factory-relationships)
    - [Has Many Relationships](#has-many-relationships)
    - [Belongs To Relationships](#belongs-to-relationships)
    - [Many To Many Relationships](#many-to-many-relationships)
    - [Polymorphic Relationships](#polymorphic-relationships)
    - [Defining Relationships Within Factories](#defining-relationships-within-factories)
    - [Recycling An Existing Model For Relationships](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When testing your application or seeding your database, you may need to insert a few records into your database. Instead of manually specifying the value of each column, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/9.x/eloquent) using model factories. -->
アプリケーションをテストするとき、またはデータベースをシードするとき、データベースにいくつかのレコードを挿入する必要がある場合があります。各列の値を手動で指定する代わりに、Laravel では、モデルファクトリーを使用して、[Eloquent models](/docs/9.x/eloquent) ごとにデフォルト属性のセットを定義できます。

<!-- To see an example of how to write a factory, take a look at the `database/factories/UserFactory.php` file in your application. This factory is included with all new Laravel applications and contains the following factory definition: -->
ファクトリの作成方法の例を確認するには、アプリケーション内の `database/factories/UserFactory.php` ファイルを見てください。このファクトリはすべての新しい Laravel アプリケーションに含まれており、次のファクトリ定義が含まれています。

```
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

<!-- As you can see, in their most basic form, factories are classes that extend Laravel's base factory class and define a `definition` method. The `definition` method returns the default set of attribute values that should be applied when creating a model using the factory. -->
ご覧のとおり、最も基本的な形式では、ファクトリは Laravel の基本ファクトリ クラスを拡張し、`definition` メソッドを定義するクラスです。 `definition` メソッドは、ファクトリを使用してモデルを作成するときに適用する必要がある属性値のデフォルトのセットを返します。

<!-- Via the `fake` helper, factories have access to the [Faker](https://github.com/FakerPHP/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing and seeding. -->
`fake` ヘルパを介して、ファクトリは [Faker](https://github.com/FakerPHP/Faker) PHP ライブラリにアクセスできるため、テストやシード用にさまざまな種類のランダム データを簡単に生成できます。

> [!NOTE]
> `faker_locale` オプションを `config/app.php` 構成ファイルに追加することで、アプリケーションの Faker ロケールを設定できます。

<a name="defining-model-factories"></a>
<!-- ## Defining Model Factories -->
## Defining Model Factories

<a name="generating-factories"></a>
<!-- ### Generating Factories -->
### Generating Factories

<!-- To create a factory, execute the `make:factory` [Artisan command](/docs/9.x/artisan): -->
ファクトリを作成するには、`make:factory` [Artisan command](/docs/9.x/artisan) を実行します。

```shell
php artisan make:factory PostFactory
```

<!-- The new factory class will be placed in your `database/factories` directory. -->
新しいファクトリ クラスは、`database/factories` ディレクトリに配置されます。

<a name="factory-and-model-discovery-conventions"></a>
<!-- #### Model & Factory Discovery Conventions -->
#### Model & Factory Discovery Conventions

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. -->
ファクトリを定義したら、`Illuminate\Database\Eloquent\Factories\HasFactory` トレイトによってモデルに提供される静的 `factory` メソッドを使用して、そのモデルのファクトリ インスタンスをインスタンス化できます。

<!-- The `HasFactory` trait's `factory` method will use conventions to determine the proper factory for the model the trait is assigned to. Specifically, the method will look for a factory in the `Database\Factories` namespace that has a class name matching the model name and is suffixed with `Factory`. If these conventions do not apply to your particular application or factory, you may overwrite the `newFactory` method on your model to return an instance of the model's corresponding factory directly: -->
`HasFactory` トレイトの `factory` メソッドは、規約を使用して、トレイトが割り当てられているモデルに適切なファクトリを決定します。具体的には、このメソッドは、モデル名と一致するクラス名を持ち、接尾辞が `Factory` である `Database\Factories` 名前空間内のファクトリを検索します。これらの規則が特定のアプリケーションまたはファクトリに適用されない場合は、モデルの `newFactory` メソッドを上書きして、モデルの対応するファクトリのインスタンスを直接返すことができます。

```
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

<!-- Next, define a `model` property on the corresponding factory: -->
次に、対応するファクトリで `model` プロパティを定義します。

```
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
<!-- ### Factory States -->
### Factory States

<!-- State manipulation methods allow you to define discrete modifications that can be applied to your model factories in any combination. For example, your `Database\Factories\UserFactory` factory might contain a `suspended` state method that modifies one of its default attribute values. -->
状態操作メソッドを使用すると、モデル ファクトリに任意の組み合わせで適用できる個別の変更を定義できます。たとえば、`Database\Factories\UserFactory` ファクトリには、デフォルトの属性値の 1 つを変更する `suspended` 状態メソッドが含まれる場合があります。

<!-- State transformation methods typically call the `state` method provided by Laravel's base factory class. The `state` method accepts a closure which will receive the array of raw attributes defined for the factory and should return an array of attributes to modify: -->
状態変換メソッドは通常、Laravel の基本ファクトリ クラスによって提供される `state` メソッドを呼び出します。 `state` メソッドは、ファクトリに定義された生の属性の配列を受け取るクロージャーを受け入れ、変更する属性の配列を返す必要があります。

```
/**
 * Indicate that the user is suspended.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
public function suspended()
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<!-- #### "Trashed" State -->
#### "Trashed" State

<!-- If your Eloquent model can be [soft deleted](/docs/9.x/eloquent#soft-deleting), you may invoke the built-in `trashed` state method to indicate that the created model should already be "soft deleted". You do not need to manually define the `trashed` state as it is automatically available to all factories: -->
Eloquent モデルが [soft deleted](/docs/9.x/eloquent#soft-deleting) である可能性がある場合は、組み込みの `trashed` 状態メソッドを呼び出して、作成されたモデルがすでに「論理的に削除」されている必要があることを示すことができます。 `trashed` 状態はすべてのファクトリで自動的に使用できるため、手動で定義する必要はありません。

```
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
<!-- ### Factory Callbacks -->
### Factory Callbacks

<!-- Factory callbacks are registered using the `afterMaking` and `afterCreating` methods and allow you to perform additional tasks after making or creating a model. You should register these callbacks by defining a `configure` method on your factory class. This method will be automatically called by Laravel when the factory is instantiated: -->
ファクトリ コールバックは、`afterMaking` メソッドと `afterCreating` メソッドを使用して登録され、モデルの作成後に追加のタスクを実行できるようになります。ファクトリ クラスで `configure` メソッドを定義して、これらのコールバックを登録する必要があります。このメソッドは、ファクトリがインスタンス化されるときに Laravel によって自動的に呼び出されます。

```
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     *
     * @return $this
     */
    public function configure()
    {
        return $this->afterMaking(function (User $user) {
            //
        })->afterCreating(function (User $user) {
            //
        });
    }

    // ...
}
```

<a name="creating-models-using-factories"></a>
<!-- ## Creating Models Using Factories -->
## Creating Models Using Factories

<a name="instantiating-models"></a>
<!-- ### Instantiating Models -->
### Instantiating Models

<!-- Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. Let's take a look at a few examples of creating models. First, we'll use the `make` method to create models without persisting them to the database: -->
ファクトリを定義したら、`Illuminate\Database\Eloquent\Factories\HasFactory` トレイトによってモデルに提供される静的 `factory` メソッドを使用して、そのモデルのファクトリ インスタンスをインスタンス化できます。モデル作成の例をいくつか見てみましょう。まず、`make` メソッドを使用して、モデルをデータベースに保存せずに作成します。

```
use App\Models\User;

$user = User::factory()->make();
```

<!-- You may create a collection of many models using the `count` method: -->
`count` メソッドを使用して、多くのモデルのコレクションを作成できます。

```
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
<!-- #### Applying States -->
#### Applying States

<!-- You may also apply any of your [states](#factory-states) to the models. If you would like to apply multiple state transformations to the models, you may simply call the state transformation methods directly: -->
[states](#factory-states) のいずれかをモデルに適用することもできます。複数の状態変換をモデルに適用したい場合は、状態変換メソッドを直接呼び出すだけです。

```
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
<!-- #### Overriding Attributes -->
#### Overriding Attributes

<!-- If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified attributes will be replaced while the rest of the attributes remain set to their default values as specified by the factory: -->
モデルのデフォルト値の一部をオーバーライドしたい場合は、値の配列を `make` メソッドに渡すことができます。指定された属性のみが置換され、残りの属性は工場で指定されたデフォルト値に設定されたままになります。

```
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

<!-- Alternatively, the `state` method may be called directly on the factory instance to perform an inline state transformation: -->
あるいは、`state` メソッドをファクトリ インスタンスで直接呼び出して、インライン状態変換を実行することもできます。

```
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> ファクトリを使用してモデルを作成する場合、[Mass assignment protection](/docs/9.x/eloquent#mass-assignment) は自動的に無効になります。

<a name="persisting-models"></a>
<!-- ### Persisting Models -->
### Persisting Models

<!-- The `create` method instantiates model instances and persists them to the database using Eloquent's `save` method: -->
`create` メソッドはモデル インスタンスをインスタンス化し、Eloquent の `save` メソッドを使用してデータベースに永続化します。

```
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```

<!-- You may override the factory's default model attributes by passing an array of attributes to the `create` method: -->
属性の配列を `create` メソッドに渡すことで、ファクトリのデフォルトのモデル属性をオーバーライドできます。

```
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
<!-- ### Sequences -->
### Sequences

<!-- Sometimes you may wish to alternate the value of a given model attribute for each created model. You may accomplish this by defining a state transformation as a sequence. For example, you may wish to alternate the value of an `admin` column between `Y` and `N` for each created user: -->
場合によっては、作成されたモデルごとに特定のモデル属性の値を変更したい場合があります。これは、状態変換をシーケンスとして定義することで実現できます。たとえば、作成されたユーザーごとに、`admin` 列の値を `Y` と `N` の間で切り替えることができます。

```
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

<!-- In this example, five users will be created with an `admin` value of `Y` and five users will be created with an `admin` value of `N`. -->
この例では、`admin` 値 `Y` で 5 人のユーザーが作成され、`admin` 値 `N` で 5 人のユーザーが作成されます。

<!-- If necessary, you may include a closure as a sequence value. The closure will be invoked each time the sequence needs a new value: -->
必要に応じて、シーケンス値としてクロージャを含めることができます。クロージャは、シーケンスに新しい値が必要になるたびに呼び出されます。

```
$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn ($sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

<!-- Within a sequence closure, you may access the `$index` or `$count` properties on the sequence instance that is injected into the closure. The `$index` property contains the number of iterations through the sequence that have occurred thus far, while the `$count` property contains the total number of times the sequence will be invoked: -->
シーケンス クロージャ内では、クロージャに挿入されるシーケンス インスタンスの `$index` プロパティまたは `$count` プロパティにアクセスできます。 `$index` プロパティには、これまでに発生したシーケンスの反復回数が含まれ、`$count` プロパティには、シーケンスが呼び出される合計回数が含まれます。

```
$users = User::factory()
                ->count(10)
                ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

<!-- For convenience, sequences may also be applied using the `sequence` method, which simply invokes the `state` method internally. The `sequence` method accepts a closure or arrays of sequenced attributes: -->
便宜上、`sequence` メソッドを使用してシーケンスを適用することもできます。これは単に `state` メソッドを内部で呼び出すだけです。 `sequence` メソッドは、クロージャまたはシーケンスされた属性の配列を受け入れます。

```
$users = User::factory()
                ->count(2)
                ->sequence(
                    ['name' => 'First User'],
                    ['name' => 'Second User'],
                )
                ->create();
```

<a name="factory-relationships"></a>
<!-- ## Factory Relationships -->
## Factory Relationships

<a name="has-many-relationships"></a>
<!-- ### Has Many Relationships -->
### Has Many Relationships

<!-- Next, let's explore building Eloquent model relationships using Laravel's fluent factory methods. First, let's assume our application has an `App\Models\User` model and an `App\Models\Post` model. Also, let's assume that the `User` model defines a `hasMany` relationship with `Post`. We can create a user that has three posts using the `has` method provided by the Laravel's factories. The `has` method accepts a factory instance: -->
次に、Laravel の Fluent Factory メソッドを使用して Eloquent モデルの関係を構築してみましょう。まず、アプリケーションに `App\Models\User` モデルと `App\Models\Post` モデルがあると仮定します。また、`User` モデルが `Post` との `hasMany` 関係を定義すると仮定します。 Laravel のファクトリーが提供する `has` メソッドを使用して、3 つの投稿を持つユーザーを作成できます。 `has` メソッドはファクトリ インスタンスを受け入れます。

```
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

<!-- By convention, when passing a `Post` model to the `has` method, Laravel will assume that the `User` model must have a `posts` method that defines the relationship. If necessary, you may explicitly specify the name of the relationship that you would like to manipulate: -->
慣例により、`Post` モデルを `has` メソッドに渡すとき、Laravel は、`User` モデルには関係を定義する `posts` メソッドが必要であると想定します。必要に応じて、操作する関係の名前を明示的に指定できます。

```
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

<!-- Of course, you may perform state manipulations on the related models. In addition, you may pass a closure based state transformation if your state change requires access to the parent model: -->
もちろん、関連するモデルに対して状態操作を実行することもできます。さらに、状態変更で親モデルへのアクセスが必要な場合は、クロージャ ベースの状態変換を渡すことができます。

```
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
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to build relationships. For example, the following example will use convention to determine that the related models should be created via a `posts` relationship method on the `User` model: -->
便宜上、Laravel のマジックファクトリー関係メソッドを使用して関係を構築できます。たとえば、次の例では、規則を使用して、`User` モデルの `posts` リレーションシップ メソッドを介して関連モデルを作成する必要があることを決定します。

```
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

<!-- When using magic methods to create factory relationships, you may pass an array of attributes to override on the related models: -->
マジック メソッドを使用してファクトリ リレーションシップを作成する場合、関連モデルをオーバーライドする属性の配列を渡すことができます。

```
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

<!-- You may provide a closure based state transformation if your state change requires access to the parent model: -->
状態変更で親モデルへのアクセスが必要な場合は、クロージャ ベースの状態変換を提供できます。

```
$user = User::factory()
            ->hasPosts(3, function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
            ->create();
```

<a name="belongs-to-relationships"></a>
<!-- ### Belongs To Relationships -->
### Belongs To Relationships

<!-- Now that we have explored how to build "has many" relationships using factories, let's explore the inverse of the relationship. The `for` method may be used to define the parent model that factory created models belong to. For example, we can create three `App\Models\Post` model instances that belong to a single user: -->
ファクトリを使用して「has many」関係を構築する方法を説明したので、その逆の関係を見てみましょう。 `for` メソッドは、工場で作成されたモデルが属する親モデルを定義するために使用できます。たとえば、1 人のユーザーに属する 3 つの `App\Models\Post` モデル インスタンスを作成できます。

```
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
            ->count(3)
            ->for(User::factory()->state([
                'name' => 'Jessica Archer',
            ]))
            ->create();
```

<!-- If you already have a parent model instance that should be associated with the models you are creating, you may pass the model instance to the `for` method: -->
作成中のモデルに関連付ける親モデル インスタンスがすでにある場合は、そのモデル インスタンスを `for` メソッドに渡すことができます。

```
$user = User::factory()->create();

$posts = Post::factory()
            ->count(3)
            ->for($user)
            ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to define "belongs to" relationships. For example, the following example will use convention to determine that the three posts should belong to the `user` relationship on the `Post` model: -->
便宜上、Laravel のマジックファクトリー関係メソッドを使用して、「所属する」関係を定義できます。たとえば、次の例では、規則を使用して、3 つの投稿が `Post` モデルの `user` 関係に属する必要があることを決定します。

```
$posts = Post::factory()
            ->count(3)
            ->forUser([
                'name' => 'Jessica Archer',
            ])
            ->create();
```

<a name="many-to-many-relationships"></a>
<!-- ### Many To Many Relationships -->
### Many To Many Relationships

<!-- Like [has many relationships](#has-many-relationships), "many to many" relationships may be created using the `has` method: -->
[has many relationships](#has-many-relationships) と同様に、「多対多」関係は `has` メソッドを使用して作成できます。

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->has(Role::factory()->count(3))
            ->create();
```

<a name="pivot-table-attributes"></a>
<!-- #### Pivot Table Attributes -->
#### Pivot Table Attributes

<!-- If you need to define attributes that should be set on the pivot / intermediate table linking the models, you may use the `hasAttached` method. This method accepts an array of pivot table attribute names and values as its second argument: -->
モデルをリンクするピボット/中間テーブルに設定する必要がある属性を定義する必要がある場合は、`hasAttached` メソッドを使用できます。このメソッドは、ピボット テーブルの属性名と値の配列を 2 番目の引数として受け入れます。

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->hasAttached(
                Role::factory()->count(3),
                ['active' => true]
            )
            ->create();
```

<!-- You may provide a closure based state transformation if your state change requires access to the related model: -->
状態変更に関連モデルへのアクセスが必要な場合は、クロージャ ベースの状態変換を提供できます。

```
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

<!-- If you already have model instances that you would like to be attached to the models you are creating, you may pass the model instances to the `hasAttached` method. In this example, the same three roles will be attached to all three users: -->
作成中のモデルにアタッチしたいモデル インスタンスが既にある場合は、そのモデル インスタンスを `hasAttached` メソッドに渡すことができます。この例では、同じ 3 つのロールが 3 人のユーザー全員にアタッチされます。

```
$roles = Role::factory()->count(3)->create();

$user = User::factory()
            ->count(3)
            ->hasAttached($roles, ['active' => true])
            ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
<!-- #### Using Magic Methods -->
#### Using Magic Methods

<!-- For convenience, you may use Laravel's magic factory relationship methods to define many to many relationships. For example, the following example will use convention to determine that the related models should be created via a `roles` relationship method on the `User` model: -->
便宜上、Laravel のマジックファクトリー関係メソッドを使用して多対多の関係を定義できます。たとえば、次の例では、規則を使用して、`User` モデルの `roles` リレーションシップ メソッドを介して関連モデルを作成する必要があることを決定します。

```
$user = User::factory()
            ->hasRoles(1, [
                'name' => 'Editor'
            ])
            ->create();
```

<a name="polymorphic-relationships"></a>
<!-- ### Polymorphic Relationships -->
### Polymorphic Relationships

<!-- [Polymorphic relationships](/docs/9.x/eloquent-relationships#polymorphic-relationships) may also be created using factories. Polymorphic "morph many" relationships are created in the same way as typical "has many" relationships. For example, if a `App\Models\Post` model has a `morphMany` relationship with a `App\Models\Comment` model: -->
[Polymorphic relationships](/docs/9.x/eloquent-relationships#polymorphic-relationships) は、ファクトリを使用して作成することもできます。ポリモーフィックな「モーフ・メニー」リレーションシップは、典型的な「ハズ・メニー」リレーションシップと同じ方法で作成されます。たとえば、`App\Models\Post` モデルに `App\Models\Comment` モデルとの `morphMany` 関係がある場合、次のようになります。

```
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
<!-- #### Morph To Relationships -->
#### Morph To Relationships

<!-- Magic methods may not be used to create `morphTo` relationships. Instead, the `for` method must be used directly and the name of the relationship must be explicitly provided. For example, imagine that the `Comment` model has a `commentable` method that defines a `morphTo` relationship. In this situation, we may create three comments that belong to a single post by using the `for` method directly: -->
`morphTo` 関係の作成にマジック メソッドを使用することはできません。代わりに、`for` メソッドを直接使用し、関係の名前を明示的に指定する必要があります。たとえば、`Comment` モデルに、`morphTo` 関係を定義する `commentable` メソッドがあると想像してください。この状況では、`for` メソッドを直接使用して、1 つの投稿に属する 3 つのコメントを作成できます。

```
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
<!-- #### Polymorphic Many To Many Relationships -->
#### Polymorphic Many To Many Relationships

<!-- Polymorphic "many to many" (`morphToMany` / `morphedByMany`) relationships may be created just like non-polymorphic "many to many" relationships: -->
ポリモーフィックな「多対多」(`morphToMany` / `morphedByMany`) 関係は、非ポリモーフィックな「多対多」関係と同様に作成できます。

```
use App\Models\Tag;
use App\Models\Video;

$videos = Video::factory()
            ->hasAttached(
                Tag::factory()->count(3),
                ['public' => true]
            )
            ->create();
```

<!-- Of course, the magic `has` method may also be used to create polymorphic "many to many" relationships: -->
もちろん、魔法の `has` メソッドを使用して、多態性の「多対多」関係を作成することもできます。

```
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
<!-- ### Defining Relationships Within Factories -->
### Defining Relationships Within Factories

<!-- To define a relationship within your model factory, you will typically assign a new factory instance to the foreign key of the relationship. This is normally done for the "inverse" relationships such as `belongsTo` and `morphTo` relationships. For example, if you would like to create a new user when creating a post, you may do the following: -->
モデル ファクトリ内でリレーションシップを定義するには、通常、リレーションシップの外部キーに新しいファクトリ インスタンスを割り当てます。これは通常、`belongsTo` 関係や `morphTo` 関係などの「逆」関係に対して行われます。たとえば、投稿の作成時に新しいユーザーを作成したい場合は、次の手順を実行します。

```
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array
 */
public function definition()
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<!-- If the relationship's columns depend on the factory that defines it you may assign a closure to an attribute. The closure will receive the factory's evaluated attribute array: -->
リレーションシップの列がそれを定義するファクトリに依存する場合は、属性にクロージャを割り当てることができます。クロージャはファクトリの評価された属性配列を受け取ります。

```
/**
 * Define the model's default state.
 *
 * @return array
 */
public function definition()
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
<!-- ### Recycling An Existing Model For Relationships -->
### Recycling An Existing Model For Relationships

<!-- If you have models that share a common relationship with another model, you may use the `recycle` method to ensure a single instance of the related model is recycled for all of the relationships created by the factory. -->
別のモデルと共通の関係を共有するモデルがある場合は、`recycle` メソッドを使用して、関連モデルの単一インスタンスがファクトリによって作成されたすべての関係に対して確実にリサイクルされるようにすることができます。

<!-- For example, imagine you have `Airline`, `Flight`, and `Ticket` models, where the ticket belongs to an airline and a flight, and the flight also belongs to an airline. When creating tickets, you will probably want the same airline for both the ticket and the flight, so you may pass an airline instance to the `recycle` method: -->
たとえば、`Airline`、`Flight`、および `Ticket` モデルがあり、チケットが航空会社とフライトに属し、フライトも航空会社に属しているとします。チケットを作成するときは、おそらくチケットとフライトの両方に同じ航空会社が必要になるため、航空会社インスタンスを `recycle` メソッドに渡すことができます。

```
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

<!-- You may find the `recycle` method particularly useful if you have models belonging to a common user or team. -->
`recycle` メソッドは、共通のユーザーまたはチームに属するモデルがある場合に特に便利です。

<!-- The `recycle` method also accepts a collection of existing models. When a collection is provided to the `recycle` method, a random model from the collection will be chosen when the factory needs a model of that type: -->
`recycle` メソッドは、既存のモデルのコレクションも受け入れます。コレクションが `recycle` メソッドに提供されると、ファクトリがそのタイプのモデルを必要とするときに、コレクションからランダムなモデルが選択されます。

```
Ticket::factory()
    ->recycle($airlines)
    ->create();
```

