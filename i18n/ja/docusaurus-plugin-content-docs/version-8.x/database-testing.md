# データベースのテスト (Database Testing)

- [Introduction](#introduction)
    - [各テスト後のデータベースのリセット](#resetting-the-database-after-each-test)
- [モデルファクトリーの定義](#defining-model-factories)
    - [コンセプトの概要](#concept-overview)
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
- [シーダーの実行](#running-seeders)
- [利用可能なアサーション](#available-assertions)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、データベース駆動型アプリケーションのテストを容易にするさまざまな便利なツールとアサーションを提供します。さらに、Laravel モデル ファクトリとシーダーにより、アプリケーションの Eloquent モデルとリレーションシップを使用してテスト データベース レコードを簡単に作成できます。これらの強力な機能については、次のドキュメントで説明します。

<a name="resetting-the-database-after-each-test"></a>
### 各テスト後のデータベースのリセット

さらに先に進む前に、前のテストのデータが後続のテストに干渉しないように、各テストの後にデータベースをリセットする方法について説明します。 Laravel に含まれる `Illuminate\Foundation\Testing\RefreshDatabase` トレイトがこれを処理します。テストクラスでトレイトを使用するだけです。

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function test_basic_example()
        {
            $response = $this->get('/');

            // ...
        }
    }

<a name="defining-model-factories"></a>
## モデルファクトリーの定義 (Defining Model Factories)

<a name="concept-overview"></a>
### コンセプトの概要

まず、Eloquent モデル ファクトリーについて話しましょう。テストする場合、テストを実行する前にデータベースにいくつかのレコードを挿入する必要がある場合があります。このテストデータを作成するときに各列の値を手動で指定する代わりに、Laravel ではモデルファクトリーを使用して [Eloquent モデル](/docs/{{version}}/eloquent) ごとにデフォルト属性のセットを定義できます。

ファクトリの作成方法の例を確認するには、アプリケーション内の `database/factories/UserFactory.php` ファイルを見てください。このファクトリはすべての新しい Laravel アプリケーションに含まれており、次のファクトリ定義が含まれています。

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
                'name' => $this->faker->name(),
                'email' => $this->faker->unique()->safeEmail(),
                'email_verified_at' => now(),
                'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
                'remember_token' => Str::random(10),
            ];
        }
    }

ご覧のとおり、最も基本的な形式では、ファクトリは Laravel の基本ファクトリ クラスを拡張し、`definition` メソッドを定義するクラスです。 `definition` メソッドは、ファクトリを使用してモデルを作成するときに適用する必要がある属性値のデフォルトのセットを返します。

`faker` プロパティを介して、ファクトリは [Faker](https://github.com/FakerPHP/Faker) PHP ライブラリにアクセスできるため、テスト用にさまざまな種類のランダム データを簡単に生成できます。

> {tip} `config/app.php` 構成ファイルに `faker_locale` オプションを追加することで、アプリケーションの Faker ロケールを設定できます。

<a name="generating-factories"></a>
### 工場の生成

ファクトリを作成するには、`make:factory` [Artisan コマンド](/docs/{{version}}/artisan) を実行します。

    php artisan make:factory PostFactory

新しいファクトリ クラスは、`database/factories` ディレクトリに配置されます。

<a name="factory-and-model-discovery-conventions"></a>
#### モデルとファクトリーのディスカバリー規約

ファクトリを定義したら、`Illuminate\Database\Eloquent\Factories\HasFactory` トレイトによってモデルに提供される静的 `factory` メソッドを使用して、そのモデルのファクトリ インスタンスをインスタンス化できます。

`HasFactory` トレイトの `factory` メソッドは、規約を使用して、トレイトが割り当てられているモデルに適切なファクトリを決定します。具体的には、このメソッドは、モデル名と一致するクラス名を持ち、接尾辞が `Factory` である `Database\Factories` 名前空間内のファクトリを検索します。これらの規則が特定のアプリケーションまたはファクトリに適用されない場合は、モデルの `newFactory` メソッドを上書きして、モデルの対応するファクトリのインスタンスを直接返すことができます。

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

次に、対応するファクトリで `model` プロパティを定義します。

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

<a name="factory-states"></a>
### 工場出荷時の状態

状態操作メソッドを使用すると、モデル ファクトリに任意の組み合わせで適用できる個別の変更を定義できます。たとえば、`Database\Factories\UserFactory` ファクトリには、デフォルトの属性値の 1 つを変更する `suspended` 状態メソッドが含まれる場合があります。

状態変換メソッドは通常、Laravel の基本ファクトリ クラスによって提供される `state` メソッドを呼び出します。 `state` メソッドは、ファクトリに定義された生の属性の配列を受け取るクロージャーを受け入れ、変更する属性の配列を返す必要があります。

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

<a name="factory-callbacks"></a>
### ファクトリーコールバック

ファクトリ コールバックは、`afterMaking` メソッドと `afterCreating` メソッドを使用して登録され、モデルの作成後に追加のタスクを実行できるようになります。ファクトリ クラスで `configure` メソッドを定義して、これらのコールバックを登録する必要があります。このメソッドは、ファクトリがインスタンス化されるときに Laravel によって自動的に呼び出されます。

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

<a name="creating-models-using-factories"></a>
## ファクトリを使用したモデルの作成 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### モデルのインスタンス化

ファクトリを定義したら、`Illuminate\Database\Eloquent\Factories\HasFactory` トレイトによってモデルに提供される静的 `factory` メソッドを使用して、そのモデルのファクトリ インスタンスをインスタンス化できます。モデル作成の例をいくつか見てみましょう。まず、`make` メソッドを使用して、モデルをデータベースに保存せずに作成します。

    use App\Models\User;

    public function test_models_can_be_instantiated()
    {
        $user = User::factory()->make();

        // Use model in tests...
    }

`count` メソッドを使用して、多くのモデルのコレクションを作成できます。

    $users = User::factory()->count(3)->make();

<a name="applying-states"></a>
#### 状態の適用

[states](#factory-states) のいずれかをモデルに適用することもできます。複数の状態変換をモデルに適用したい場合は、状態変換メソッドを直接呼び出すだけです。

    $users = User::factory()->count(5)->suspended()->make();

<a name="overriding-attributes"></a>
#### 属性の上書き

モデルのデフォルト値の一部をオーバーライドしたい場合は、値の配列を `make` メソッドに渡すことができます。指定された属性のみが置換され、残りの属性は工場で指定されたデフォルト値に設定されたままになります。

    $user = User::factory()->make([
        'name' => 'Abigail Otwell',
    ]);

あるいは、`state` メソッドをファクトリ インスタンスで直接呼び出して、インライン状態変換を実行することもできます。

    $user = User::factory()->state([
        'name' => 'Abigail Otwell',
    ])->make();

> {tip} ファクトリを使用してモデルを作成する場合、[一括割り当ての保護](/docs/{{version}}/eloquent#mass-assignment) は自動的に無効になります。

<a name="persisting-models"></a>
### 永続的なモデル

`create` メソッドはモデル インスタンスをインスタンス化し、Eloquent の `save` メソッドを使用してデータベースに永続化します。

    use App\Models\User;

    public function test_models_can_be_persisted()
    {
        // Create a single App\Models\User instance...
        $user = User::factory()->create();

        // Create three App\Models\User instances...
        $users = User::factory()->count(3)->create();

        // Use model in tests...
    }

属性の配列を `create` メソッドに渡すことで、ファクトリのデフォルトのモデル属性をオーバーライドできます。

    $user = User::factory()->create([
        'name' => 'Abigail',
    ]);

<a name="sequences"></a>
### シーケンス

場合によっては、作成されたモデルごとに特定のモデル属性の値を変更したい場合があります。これは、状態変換をシーケンスとして定義することで実現できます。たとえば、作成されたユーザーごとに、`admin` 列の値を `Y` と `N` の間で切り替えることができます。

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Sequence;

    $users = User::factory()
                    ->count(10)
                    ->state(new Sequence(
                        ['admin' => 'Y'],
                        ['admin' => 'N'],
                    ))
                    ->create();

この例では、`admin` 値 `Y` で 5 人のユーザーが作成され、`admin` 値 `N` で 5 人のユーザーが作成されます。

必要に応じて、シーケンス値としてクロージャを含めることができます。クロージャは、シーケンスに新しい値が必要になるたびに呼び出されます。

    $users = User::factory()
                    ->count(10)
                    ->state(new Sequence(
                        fn ($sequence) => ['role' => UserRoles::all()->random()],
                    ))
                    ->create();

シーケンス クロージャ内では、クロージャに挿入されるシーケンス インスタンスの `$index` プロパティまたは `$count` プロパティにアクセスできます。 `$index` プロパティには、これまでに発生したシーケンスの反復回数が含まれ、`$count` プロパティには、シーケンスが呼び出される合計回数が含まれます。

    $users = User::factory()
                    ->count(10)
                    ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                    ->create();

<a name="factory-relationships"></a>
## 工場との関係 (Factory Relationships)

<a name="has-many-relationships"></a>
### 多くの関係がある

次に、Laravel の Fluent Factory メソッドを使用して Eloquent モデルの関係を構築してみましょう。まず、アプリケーションに `App\Models\User` モデルと `App\Models\Post` モデルがあると仮定します。また、`User` モデルが `Post` との `hasMany` 関係を定義すると仮定します。 Laravel のファクトリーが提供する `has` メソッドを使用して、3 つの投稿を持つユーザーを作成できます。 `has` メソッドはファクトリ インスタンスを受け入れます。

    use App\Models\Post;
    use App\Models\User;

    $user = User::factory()
                ->has(Post::factory()->count(3))
                ->create();

慣例により、`Post` モデルを `has` メソッドに渡すとき、Laravel は、`User` モデルには関係を定義する `posts` メソッドが必要であると想定します。必要に応じて、操作する関係の名前を明示的に指定できます。

    $user = User::factory()
                ->has(Post::factory()->count(3), 'posts')
                ->create();

もちろん、関連するモデルに対して状態操作を実行することもできます。さらに、状態変更で親モデルへのアクセスが必要な場合は、クロージャ ベースの状態変換を渡すことができます。

    $user = User::factory()
                ->has(
                    Post::factory()
                            ->count(3)
                            ->state(function (array $attributes, User $user) {
                                return ['user_type' => $user->type];
                            })
                )
                ->create();

<a name="has-many-relationships-using-magic-methods"></a>
#### 魔法の方法を使用する

便宜上、Laravel のマジックファクトリー関係メソッドを使用して関係を構築できます。たとえば、次の例では、規則を使用して、`User` モデルの `posts` リレーションシップ メソッドを介して関連モデルを作成する必要があることを決定します。

    $user = User::factory()
                ->hasPosts(3)
                ->create();

マジック メソッドを使用してファクトリ リレーションシップを作成する場合、関連モデルをオーバーライドする属性の配列を渡すことができます。

    $user = User::factory()
                ->hasPosts(3, [
                    'published' => false,
                ])
                ->create();

状態変更で親モデルへのアクセスが必要な場合は、クロージャ ベースの状態変換を提供できます。

    $user = User::factory()
                ->hasPosts(3, function (array $attributes, User $user) {
                    return ['user_type' => $user->type];
                })
                ->create();

<a name="belongs-to-relationships"></a>
### 関係に属します

ファクトリを使用して「has many」関係を構築する方法を説明したので、その逆の関係を見てみましょう。 `for` メソッドは、工場で作成されたモデルが属する親モデルを定義するために使用できます。たとえば、1 人のユーザーに属する 3 つの `App\Models\Post` モデル インスタンスを作成できます。

    use App\Models\Post;
    use App\Models\User;

    $posts = Post::factory()
                ->count(3)
                ->for(User::factory()->state([
                    'name' => 'Jessica Archer',
                ]))
                ->create();

作成中のモデルに関連付ける親モデル インスタンスがすでにある場合は、そのモデル インスタンスを `for` メソッドに渡すことができます。

    $user = User::factory()->create();

    $posts = Post::factory()
                ->count(3)
                ->for($user)
                ->create();

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 魔法の方法を使用する

便宜上、Laravel のマジックファクトリー関係メソッドを使用して、「所属する」関係を定義できます。たとえば、次の例では、規則を使用して、3 つの投稿が `Post` モデルの `user` 関係に属する必要があることを決定します。

    $posts = Post::factory()
                ->count(3)
                ->forUser([
                    'name' => 'Jessica Archer',
                ])
                ->create();

<a name="many-to-many-relationships"></a>
### 多対多の関係

[多くの関係がある](#has-many-relationships) と同様に、「多対多」関係は `has` メソッドを使用して作成できます。

    use App\Models\Role;
    use App\Models\User;

    $user = User::factory()
                ->has(Role::factory()->count(3))
                ->create();

<a name="pivot-table-attributes"></a>
#### ピボットテーブルの属性

モデルをリンクするピボット/中間テーブルに設定する必要がある属性を定義する必要がある場合は、`hasAttached` メソッドを使用できます。このメソッドは、ピボット テーブルの属性名と値の配列を 2 番目の引数として受け入れます。

    use App\Models\Role;
    use App\Models\User;

    $user = User::factory()
                ->hasAttached(
                    Role::factory()->count(3),
                    ['active' => true]
                )
                ->create();

状態変更に関連モデルへのアクセスが必要な場合は、クロージャ ベースの状態変換を提供できます。

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

作成中のモデルにアタッチしたいモデル インスタンスが既にある場合は、そのモデル インスタンスを `hasAttached` メソッドに渡すことができます。この例では、同じ 3 つのロールが 3 人のユーザー全員にアタッチされます。

    $roles = Role::factory()->count(3)->create();

    $user = User::factory()
                ->count(3)
                ->hasAttached($roles, ['active' => true])
                ->create();

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 魔法の方法を使用する

便宜上、Laravel のマジックファクトリー関係メソッドを使用して多対多の関係を定義できます。たとえば、次の例では、規則を使用して、`User` モデルの `roles` リレーションシップ メソッドを介して関連モデルを作成する必要があることを決定します。

    $user = User::factory()
                ->hasRoles(1, [
                    'name' => 'Editor'
                ])
                ->create();

<a name="polymorphic-relationships"></a>
### ポリモーフィックな関係

[ポリモーフィックな関係](/docs/{{version}}/eloquent-relationships#polymorphic-relationships) は、ファクトリを使用して作成することもできます。ポリモーフィックな「モーフ・メニー」リレーションシップは、典型的な「ハズ・メニー」リレーションシップと同じ方法で作成されます。たとえば、`App\Models\Post` モデルに `App\Models\Comment` モデルとの `morphMany` 関係がある場合、次のようになります。

    use App\Models\Post;

    $post = Post::factory()->hasComments(3)->create();

<a name="morph-to-relationships"></a>
#### 関係へのモーフ

`morphTo` 関係の作成にマジック メソッドを使用することはできません。代わりに、`for` メソッドを直接使用し、関係の名前を明示的に指定する必要があります。たとえば、`Comment` モデルに、`morphTo` 関係を定義する `commentable` メソッドがあると想像してください。この状況では、`for` メソッドを直接使用して、1 つの投稿に属する 3 つのコメントを作成できます。

    $comments = Comment::factory()->count(3)->for(
        Post::factory(), 'commentable'
    )->create();

<a name="polymorphic-many-to-many-relationships"></a>
#### ポリモーフィックな多対多の関係

ポリモーフィックな「多対多」(`morphToMany` / `morphedByMany`) 関係は、非ポリモーフィックな「多対多」関係と同様に作成できます。

    use App\Models\Tag;
    use App\Models\Video;

    $videos = Video::factory()
                ->hasAttached(
                    Tag::factory()->count(3),
                    ['public' => true]
                )
                ->create();

もちろん、魔法の `has` メソッドを使用して、多態性の「多対多」関係を作成することもできます。

    $videos = Video::factory()
                ->hasTags(3, ['public' => true])
                ->create();

<a name="defining-relationships-within-factories"></a>
### ファクトリ内の関係の定義

モデル ファクトリ内でリレーションシップを定義するには、通常、リレーションシップの外部キーに新しいファクトリ インスタンスを割り当てます。これは通常、`belongsTo` 関係や `morphTo` 関係などの「逆」関係に対して行われます。たとえば、投稿の作成時に新しいユーザーを作成したい場合は、次の手順を実行します。

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
            'title' => $this->faker->title(),
            'content' => $this->faker->paragraph(),
        ];
    }

リレーションシップの列がそれを定義するファクトリに依存する場合は、属性にクロージャを割り当てることができます。クロージャはファクトリの評価された属性配列を受け取ります。

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
            'title' => $this->faker->title(),
            'content' => $this->faker->paragraph(),
        ];
    }

<a name="running-seeders"></a>
## シーダーの実行 (Running Seeders)

機能テスト中に [データベースシーダー](/docs/{{version}}/seeding) を使用してデータベースにデータを入力する場合は、`seed` メソッドを呼び出すことができます。デフォルトでは、`seed` メソッドは `DatabaseSeeder` を実行し、これにより他のすべてのシーダーが実行されます。あるいは、特定のシーダー クラス名を `seed` メソッドに渡します。

    <?php

    namespace Tests\Feature;

    use Database\Seeders\OrderStatusSeeder;
    use Database\Seeders\TransactionStatusSeeder;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * Test creating a new order.
         *
         * @return void
         */
        public function test_orders_can_be_created()
        {
            // Run the DatabaseSeeder...
            $this->seed();

            // Run a specific seeder...
            $this->seed(OrderStatusSeeder::class);

            // ...

            // Run an array of specific seeders...
            $this->seed([
                OrderStatusSeeder::class,
                TransactionStatusSeeder::class,
                // ...
            ]);
        }
    }

あるいは、`RefreshDatabase` トレイトを使用する各テストの前にデータベースを自動的にシードするように Laravel に指示することもできます。これを行うには、基本テスト クラスで `$seed` プロパティを定義します。

    <?php

    namespace Tests;

    use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

    abstract class TestCase extends BaseTestCase
    {
        use CreatesApplication;

        /**
         * Indicates whether the default seeder should run before each test.
         *
         * @var bool
         */
        protected $seed = true;
    }

`$seed` プロパティが `true` の場合、テストは `RefreshDatabase` トレイトを使用する各テストの前に `Database\Seeders\DatabaseSeeder` クラスを実行します。ただし、テスト クラスで `$seeder` プロパティを定義することで、実行する特定のシーダーを指定できます。

    use Database\Seeders\OrderStatusSeeder;

    /**
     * Run a specific seeder before each test.
     *
     * @var string
     */
    protected $seeder = OrderStatusSeeder::class;

<a name="available-assertions"></a>
## 利用可能なアサーション (Available Assertions)

Laravel は、[PHPUnit](https://phpunit.de/) 機能テスト用にいくつかのデータベース アサーションを提供します。これらの各主張については、以下で説明します。

<a name="assert-database-count"></a>
#### アサートデータベース数

データベース内のテーブルに指定された数のレコードが含まれていることをアサートします。

    $this->assertDatabaseCount('users', 5);

<a name="assert-database-has"></a>
#### データベースにアサートがある

データベース内のテーブルに、指定されたキー/値クエリ制約に一致するレコードが含まれていることをアサートします。

    $this->assertDatabaseHas('users', [
        'email' => 'sally@example.com',
    ]);

<a name="assert-database-missing"></a>
#### アサートデータベースが見つかりません

データベース内のテーブルに、指定されたキー/値クエリ制約に一致するレコードが含まれていないことをアサートします。

    $this->assertDatabaseMissing('users', [
        'email' => 'sally@example.com',
    ]);

<a name="assert-deleted"></a>
#### アサート削除済み

`assertDeleted` は、指定された Eloquent モデルがデータベースから削除されたことをアサートします。

    use App\Models\User;

    $user = User::find(1);

    $user->delete();

    $this->assertDeleted($user);

`assertSoftDeleted` メソッドは、特定の Eloquent モデルが「論理的に削除された」ことをアサートするために使用できます。

    $this->assertSoftDeleted($user);

<a name="assert-model-exists"></a>
#### assertModelExists

指定されたモデルがデータベースに存在することをアサートします。

    use App\Models\User;

    $user = User::factory()->create();

    $this->assertModelExists($user);

<a name="assert-model-missing"></a>
#### アサートモデルが見つかりません

指定されたモデルがデータベースに存在しないことをアサートします。

    use App\Models\User;

    $user = User::factory()->create();

    $user->delete();

    $this->assertModelMissing($user);

