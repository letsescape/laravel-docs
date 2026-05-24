# データベース: シード (Database: Seeding)

- [Introduction](#introduction)
- [シーダーの作成](#writing-seeders)
    - [モデルファクトリーの使用](#using-model-factories)
    - [追加のシーダーの呼び出し](#calling-additional-seeders)
    - [モデルイベントのミュート](#muting-model-events)
- [シーダーの実行](#running-seeders)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel には、シード クラスを使用してデータベースにデータをシードする機能が含まれています。すべてのシード クラスは、`database/seeders` ディレクトリに保存されます。デフォルトでは、`DatabaseSeeder` クラスが定義されています。このクラスから、`call` メソッドを使用して他のシード クラスを実行し、シード順序を制御できます。

> **注記**
> [一括割り当ての保護](/docs/{{version}}/eloquent#mass-assignment) は、データベースのシード処理中に自動的に無効になります。

<a name="writing-seeders"></a>
## シーダーの作成 (Writing Seeders)

シーダーを生成するには、`make:seeder` [Artisan コマンド](/docs/{{version}}/artisan) を実行します。フレームワークによって生成されたすべてのシーダーは、`database/seeders` ディレクトリに配置されます。

```shell
php artisan make:seeder UserSeeder
```

シーダー クラスには、デフォルトでメソッド `run` が 1 つだけ含まれています。このメソッドは、`db:seed` [Artisan コマンド](/docs/{{version}}/artisan) が実行されるときに呼び出されます。 `run` メソッド内では、必要に応じてデータベースにデータを挿入できます。 [クエリビルダ](/docs/{{version}}/queries) を使用してデータを手動で挿入することも、[Eloquent モデル工場](/docs/{{version}}/eloquent-factories) を使用することもできます。

例として、デフォルトの `DatabaseSeeder` クラスを変更し、データベース挿入ステートメントを `run` メソッドに追加してみましょう。

    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Support\Str;

    class DatabaseSeeder extends Seeder
    {
        /**
         * Run the database seeders.
         *
         * @return void
         */
        public function run()
        {
            DB::table('users')->insert([
                'name' => Str::random(10),
                'email' => Str::random(10).'@gmail.com',
                'password' => Hash::make('password'),
            ]);
        }
    }

> **注記**
> `run` メソッドのシグネチャ内で必要な依存関係をタイプヒントで指定できます。これらは、Laravel [サービスコンテナ](/docs/{{version}}/container) を通じて自動的に解決されます。

<a name="using-model-factories"></a>
### モデルファクトリーの使用

もちろん、各モデル シードの属性を手動で指定するのは面倒です。代わりに、[モデル工場](/docs/{{version}}/eloquent-factories) を使用すると、大量のデータベース レコードを簡単に生成できます。まず、[モデルファクトリーのドキュメント](/docs/{{version}}/eloquent-factories) を確認して、ファクトリを定義する方法を学びます。

たとえば、各ユーザーが 1 つの関連投稿を持つ 50 人のユーザーを作成してみましょう。

    use App\Models\User;

    /**
     * Run the database seeders.
     *
     * @return void
     */
    public function run()
    {
        User::factory()
                ->count(50)
                ->hasPosts(1)
                ->create();
    }

<a name="calling-additional-seeders"></a>
### 追加のシーダーの呼び出し

`DatabaseSeeder` クラス内で、`call` メソッドを使用して追加のシード クラスを実行できます。 `call` メソッドを使用すると、単一のシーダー クラスが大きくなりすぎないように、データベース シードを複数のファイルに分割できます。 `call` メソッドは、実行する必要があるシーダー クラスの配列を受け取ります。

    /**
     * Run the database seeders.
     *
     * @return void
     */
    public function run()
    {
        $this->call([
            UserSeeder::class,
            PostSeeder::class,
            CommentSeeder::class,
        ]);
    }

<a name="muting-model-events"></a>
### モデルイベントのミュート

シードの実行中、モデルがイベントをディスパッチしないようにしたい場合があります。これは、`WithoutModelEvents` 特性を使用して実現できます。 `WithoutModelEvents` トレイトを使用すると、追加のシード クラスが `call` メソッド経由で実行された場合でも、モデル イベントがディスパッチされなくなります。

    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Database\Console\Seeds\WithoutModelEvents;

    class DatabaseSeeder extends Seeder
    {
        use WithoutModelEvents;

        /**
         * Run the database seeders.
         *
         * @return void
         */
        public function run()
        {
            $this->call([
                UserSeeder::class,
            ]);
        }
    }

<a name="running-seeders"></a>
## シーダーの実行 (Running Seeders)

`db:seed` Artisan コマンドを実行してデータベースをシードできます。デフォルトでは、`db:seed` コマンドは `Database\Seeders\DatabaseSeeder` クラスを実行し、このクラスが他のシード クラスを呼び出す可能性があります。ただし、`--class` オプションを使用して、個別に実行する特定のシーダー クラスを指定できます。

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

`migrate:fresh` コマンドを `--seed` オプションと組み合わせて使用​​してデータベースをシードすることもできます。これにより、すべてのテーブルが削除され、すべての移行が再実行されます。このコマンドは、データベースを完全に再構築する場合に役立ちます。 `--seeder` オプションは、実行する特定のシーダーを指定するために使用できます。

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder 
```

<a name="forcing-seeding-production"></a>
#### 本番環境でシーダーを強制的に実行する

シード操作によっては、データが変更されたり失われたりする可能性があります。実稼働データベースに対してシード コマンドを実行しないようにするために、`production` 環境でシーダーが実行される前に確認を求めるプロンプトが表示されます。プロンプトを表示せずにシーダーを強制的に実行するには、`--force` フラグを使用します。

```shell
php artisan db:seed --force
```

