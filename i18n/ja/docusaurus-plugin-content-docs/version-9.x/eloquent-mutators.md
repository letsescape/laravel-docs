# Eloquent: ミューテタとキャスティング (Eloquent: Mutators & Casting)

- [Introduction](#introduction)
- [アクセサとミューテタ](#accessors-and-mutators)
    - [アクセサの定義](#defining-an-accessor)
    - [ミューテタの定義](#defining-a-mutator)
- [属性のキャスト](#attribute-casting)
    - [配列と JSON キャスト](#array-and-json-casting)
    - [デートキャスト](#date-casting)
    - [列挙型キャスト](#enum-casting)
    - [暗号化されたキャスト](#encrypted-casting)
    - [クエリタイムキャスト](#query-time-casting)
- [カスタムキャスト](#custom-casts)
    - [値オブジェクトのキャスト](#value-object-casting)
    - [配列/JSONシリアル化](#array-json-serialization)
    - [インバウンドキャスト](#inbound-casting)
    - [キャストパラメータ](#cast-parameters)
    - [Castables](#castables)

<a name="introduction"></a>
## 導入 (Introduction)

アクセサー、ミューテタ、および属性キャストを使用すると、Eloquent 属性値をモデル インスタンスで取得または設定するときに、その値を変換できます。たとえば、[Laravel暗号化ツール](/docs/{{version}}/encryption) を使用して、データベースに保存されている値を暗号化し、Eloquent モデルでアクセスするときにその属性を自動的に復号化することができます。または、Eloquent モデル経由でアクセスするときに、データベースに保存されている JSON 文字列を配列に変換することもできます。

<a name="accessors-and-mutators"></a>
## アクセサとミューテタ (Accessors & Mutators)

<a name="defining-an-accessor"></a>
### アクセサの定義

アクセサは、アクセス時に Eloquent 属性値を変換します。アクセサーを定義するには、アクセス可能な属性を表す保護されたメソッドをモデル上に作成します。このメソッド名は、該当する場合、実際の基になるモデル属性/データベース列の「キャメル ケース」表現に対応する必要があります。

この例では、`first_name` 属性のアクセサーを定義します。アクセサーは、`first_name` 属性の値を取得しようとすると、Eloquent によって自動的に呼び出されます。すべての属性アクセサー/ミューテタ メソッドは、戻り値の型ヒント `Illuminate\Database\Eloquent\Casts\Attribute` を宣言する必要があります。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\Attribute;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Get the user's first name.
         *
         * @return \Illuminate\Database\Eloquent\Casts\Attribute
         */
        protected function firstName(): Attribute
        {
            return Attribute::make(
                get: fn ($value) => ucfirst($value),
            );
        }
    }

すべてのアクセサー メソッドは、属性へのアクセス方法と、オプションで変更する方法を定義する `Attribute` インスタンスを返します。この例では、属性にアクセスする方法のみを定義しています。これを行うには、`get` 引数を `Attribute` クラス コンストラクターに指定します。

ご覧のとおり、列の元の値がアクセサーに渡されるため、値を操作して返すことができます。アクセサーの値にアクセスするには、モデル インスタンスの `first_name` 属性にアクセスするだけです。

    use App\Models\User;

    $user = User::find(1);

    $firstName = $user->first_name;

> **注記**
> これらの計算値をモデルの配列/JSON 表現に追加したい場合は、[それらを追加する必要があります](/docs/{{version}}/eloquent-serialization#appending-values-to-json)。

<a name="building-value-objects-from-multiple-attributes"></a>
#### 複数の属性から値オブジェクトを構築する

場合によっては、アクセサーが複数のモデル属性を 1 つの「値オブジェクト」に変換する必要がある場合があります。これを行うには、`get` クロージャーは `$attributes` の 2 番目の引数を受け入れることができます。これは自動的にクロージャーに提供され、モデルの現在の属性すべての配列が含まれます。

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    );
}
```

<a name="accessor-caching"></a>
#### アクセサのキャッシュ

アクセサーから値オブジェクトを返す場合、値オブジェクトに加えられた変更は、モデルが保存される前に自動的にモデルに同期されます。これが可能なのは、Eloquent がアクセサーによって返されたインスタンスを保持し、アクセサーが呼び出されるたびに同じインスタンスを返すことができるためです。

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = 'Updated Address Line 1 Value';
    $user->address->lineTwo = 'Updated Address Line 2 Value';

    $user->save();

ただし、特に計算負荷が高い場合、文字列やブール値などのプリミティブ値のキャッシュを有効にしたい場合があります。これを実現するには、アクセサーを定義するときに `shouldCache` メソッドを呼び出します。

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn ($value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

属性のオブジェクト キャッシュ動作を無効にしたい場合は、属性を定義するときに `withoutObjectCaching` メソッドを呼び出します。

```php
/**
 * Interact with the user's address.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```

<a name="defining-a-mutator"></a>
### ミューテタの定義

ミューテタは、Eloquent 属性値が設定されているときにそれを変換します。ミューテタを定義するには、属性を定義するときに `set` 引数を指定できます。 `first_name` 属性のミューテタを定義しましょう。このミューテタは、モデルに `first_name` 属性の値を設定しようとすると自動的に呼び出されます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\Attribute;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * Interact with the user's first name.
         *
         * @return \Illuminate\Database\Eloquent\Casts\Attribute
         */
        protected function firstName(): Attribute
        {
            return Attribute::make(
                get: fn ($value) => ucfirst($value),
                set: fn ($value) => strtolower($value),
            );
        }
    }

ミューテタ クロージャーは属性に設定されている値を受け取り、値を操作して操作された値を返すことができます。ミューテタを使用するには、Eloquent モデルで `first_name` 属性を設定するだけです。

    use App\Models\User;

    $user = User::find(1);

    $user->first_name = 'Sally';

この例では、`set` コールバックが値 `Sally` で呼び出されます。次に、ミューテタは `strtolower` 関数を名前に適用し、その結果の値をモデルの内部 `$attributes` 配列に設定します。

<a name="mutating-multiple-attributes"></a>
#### 複数の属性の変更

ミューテタは、基礎となるモデルに複数の属性を設定する必要がある場合があります。これを行うには、`set` クロージャから配列を返すことができます。配列内の各キーは、モデルに関連付けられた基になる属性/データベース列に対応する必要があります。

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 *
 * @return  \Illuminate\Database\Eloquent\Casts\Attribute
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="attribute-casting"></a>
## 属性のキャスト (Attribute Casting)

属性キャストは、モデルに追加のメソッドを定義する必要なく、アクセサーやミューテタと同様の機能を提供します。代わりに、モデルの `$casts` プロパティは、属性を一般的なデータ型に変換する便利な方法を提供します。

`$casts` プロパティは、キーがキャストされる属性の名前、値が列をキャストする型である配列である必要があります。サポートされているキャスト タイプは次のとおりです。

<div class="content-list" markdown="1">

- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>10 進数:<精度></code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

</div>

属性のキャストを示すために、データベースに整数 (`0` または `1`) として保存されている `is_admin` 属性をブール値にキャストしてみましょう。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'is_admin' => 'boolean',
        ];
    }

キャストを定義した後、基になる値がデータベースに整数として格納されている場合でも、アクセス時に `is_admin` 属性は常にブール値にキャストされます。

    $user = App\Models\User::find(1);

    if ($user->is_admin) {
        //
    }

実行時に新しい一時的なキャストを追加する必要がある場合は、`mergeCasts` メソッドを使用できます。これらのキャスト定義は、モデルですでに定義されているキャストのいずれかに追加されます。

    $user->mergeCasts([
        'is_admin' => 'integer',
        'options' => 'object',
    ]);

> **警告**
> `null` の属性はキャストされません。さらに、リレーションシップと同じ名前のキャスト (または属性) を定義しないでください。

<a name="stringable-casting"></a>
#### ストリング可能な鋳造

`Illuminate\Database\Eloquent\Casts\AsStringable` キャスト クラスを使用して、モデル属性を [fluent `Illuminate\Support\Stringable` object](/docs/{{version}}/helpers#fluent-strings-method-list) にキャストできます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Casts\AsStringable;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'directory' => AsStringable::class,
        ];
    }

<a name="array-and-json-casting"></a>
### 配列と JSON キャスト

`array` キャストは、シリアル化された JSON として保存されている列を操作する場合に特に便利です。たとえば、データベースにシリアル化された JSON を含む `JSON` または `TEXT` フィールド タイプがある場合、その属性に `array` キャストを追加すると、Eloquent モデルでアクセスするときに属性が PHP 配列に自動的に逆シリアル化されます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'options' => 'array',
        ];
    }

キャストが定義されたら、`options` 属性にアクセスすると、JSON から PHP 配列に自動的に逆シリアル化されます。 `options` 属性の値を設定すると、指定された配列が自動的にシリアル化されて JSON に戻され、保存されます。

    use App\Models\User;

    $user = User::find(1);

    $options = $user->options;

    $options['key'] = 'value';

    $user->options = $options;

    $user->save();

JSON 属性の単一フィールドをより簡潔な構文で更新するには、`update` メソッドを呼び出すときに `->` 演算子を使用できます。

    $user = User::find(1);

    $user->update(['options->key' => 'value']);

<a name="array-object-and-collection-casting"></a>
#### 配列オブジェクトとコレクションのキャスト

標準の `array` キャストは多くのアプリケーションには十分ですが、いくつかの欠点があります。 `array` キャストはプリミティブ型を返すため、配列のオフセットを直接変更することはできません。たとえば、次のコードは PHP エラーをトリガーします。

    $user = User::find(1);

    $user->options['key'] = $value;

これを解決するために、Laravel は JSON 属性を [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) クラスにキャストする `AsArrayObject` キャストを提供します。この機能は、Laravel の [カスタムキャスト](#custom-casts) 実装を使用して実装されます。これにより、Laravel は、PHP エラーを引き起こすことなく個々のオフセットを変更できるように、変更されたオブジェクトをインテリジェントにキャッシュおよび変換できます。 `AsArrayObject` キャストを使用するには、それを属性に割り当てるだけです。

    use Illuminate\Database\Eloquent\Casts\AsArrayObject;

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'options' => AsArrayObject::class,
    ];

同様に、Laravel は、JSON 属性を Laravel [Collection](/docs/{{version}}/collections) インスタンスにキャストする `AsCollection` キャストを提供します。

    use Illuminate\Database\Eloquent\Casts\AsCollection;

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'options' => AsCollection::class,
    ];

<a name="date-casting"></a>
### デートキャスト

デフォルトでは、Eloquent は `created_at` 列と `updated_at` 列を [Carbon](https://github.com/briannesbitt/Carbon) のインスタンスにキャストします。これは、PHP `DateTime` クラスを拡張し、さまざまな便利なメソッドを提供します。モデルの `$casts` プロパティ配列内で追加の日付キャストを定義することで、追加の日付属性をキャストできます。通常、日付は `datetime` または `immutable_datetime` キャスト タイプを使用してキャストする必要があります。

`date` または `datetime` キャストを定義するときは、日付の形式も指定できます。この形式は、[モデルは配列または JSON にシリアル化されます](/docs/{{version}}/eloquent-serialization) の場合に使用されます。

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'created_at' => 'datetime:Y-m-d',
    ];

When a column is cast as a date, you may set the corresponding model attribute value to a UNIX timestamp, date string (`Y-m-d`), date-time string, or a `DateTime` / `Carbon` instance.日付の値は正しく変換され、データベースに保存されます。

モデルで `serializeDate` メソッドを定義することで、モデルのすべての日付のデフォルトのシリアル化形式をカスタマイズできます。この方法は、データベースに保存する際の日付の形式には影響しません。

    /**
     * Prepare a date for array / JSON serialization.
     *
     * @param  \DateTimeInterface  $date
     * @return string
     */
    protected function serializeDate(DateTimeInterface $date)
    {
        return $date->format('Y-m-d');
    }

実際にモデルの日付をデータベース内に保存するときに使用する形式を指定するには、モデルで `$dateFormat` プロパティを定義する必要があります。

    /**
     * The storage format of the model's date columns.
     *
     * @var string
     */
    protected $dateFormat = 'U';

<a name="date-casting-and-timezones"></a>
#### 日付のキャスト、シリーズ化、およびタイムゾーン

デフォルトでは、`date` および `datetime` キャストは、アプリケーションの `timezone` 構成オプションで指定されたタイムゾーンに関係なく、日付を UTC ISO-8601 日付文字列 (`1986-05-28T21:05:54.000000Z`) にシリアル化します。常にこのシリアル化形式を使用し、アプリケーションの `timezone` 構成オプションをデフォルトの `UTC` 値から変更せず、アプリケーションの日付を UTC タイムゾーンで保存することを強くお勧めします。アプリケーション全体で一貫して UTC タイムゾーンを使用すると、PHP および JavaScript で作成された他の日付操作ライブラリとの相互運用性が最大レベルで提供されます。

`datetime:Y-m-d H:i:s` などのカスタム形式が `date` または `datetime` キャストに適用される場合、日付のシリアル化中に Carbon インスタンスの内部タイムゾーンが使用されます。通常、これはアプリケーションの `timezone` 構成オプションで指定されたタイムゾーンになります。

<a name="enum-casting"></a>
### 列挙型キャスト

> **警告**
> Enum キャストは PHP 8.1 以降でのみ使用できます。

Eloquent では、属性値を PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php) にキャストすることもできます。これを実現するには、モデルの `$casts` プロパティ配列にキャストする属性と列挙型を指定します。

    use App\Enums\ServerStatus;

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'status' => ServerStatus::class,
    ];

モデルでキャストを定義すると、指定した属性は、属性を操作するときに列挙型との間で自動的にキャストされます。

    if ($server->status == ServerStatus::Provisioned) {
        $server->status = ServerStatus::Ready;

        $server->save();
    }

<a name="casting-arrays-of-enums"></a>
#### 列挙型の配列のキャスト

場合によっては、モデルで列挙値の配列を 1 つの列に格納する必要がある場合があります。これを実現するには、Laravel が提供する `AsEnumArrayObject` または `AsEnumCollection` キャストを利用できます。

    use App\Enums\ServerStatus;
    use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'statuses' => AsEnumCollection::class.':'.ServerStatus::class,
    ];

<a name="encrypted-casting"></a>
### 暗号化されたキャスト

`encrypted` キャストは、Laravel の組み込み [encryption](/docs/{{version}}/encryption) 機能を使用してモデルの属性値を暗号化します。さらに、`encrypted:array`、`encrypted:collection`、`encrypted:object`、`AsEncryptedArrayObject`、および `AsEncryptedCollection` キャストは、暗号化されていないキャストと同様に機能します。ただし、ご想像のとおり、基になる値はデータベースに保存されるときに暗号化されます。

暗号化されたテキストの最終的な長さは予測できず、対応する平文よりも長いため、関連するデータベース列が `TEXT` 型以上であることを確認してください。さらに、値はデータベース内で暗号化されるため、暗号化された属性値をクエリまたは検索することはできません。

<a name="key-rotation"></a>
#### キーのローテーション

ご存知のとおり、Laravel は、アプリケーションの `app` 構成ファイルで指定された `key` 構成値を使用して文字列を暗号化します。通常、この値は `APP_KEY` 環境変数の値に対応します。アプリケーションの暗号化キーをローテーションする必要がある場合は、新しいキーを使用して暗号化された属性を手動で再暗号化する必要があります。

<a name="query-time-casting"></a>
### クエリタイムキャスト

テーブルから生の値を選択する場合など、クエリの実行中にキャストの適用が必要になる場合があります。たとえば、次のクエリについて考えてみましょう。

    use App\Models\Post;
    use App\Models\User;

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->get();

このクエリの結果の `last_posted_at` 属性は単純な文字列になります。クエリの実行時にこの属性に `datetime` キャストを適用できれば素晴らしいでしょう。ありがたいことに、`withCasts` メソッドを使用してこれを実現できます。

    $users = User::select([
        'users.*',
        'last_posted_at' => Post::selectRaw('MAX(created_at)')
                ->whereColumn('user_id', 'users.id')
    ])->withCasts([
        'last_posted_at' => 'datetime'
    ])->get();

<a name="custom-casts"></a>
## カスタムキャスト (Custom Casts)

Laravel には、さまざまな便利なキャスト型が組み込まれています。ただし、場合によっては、独自のキャスト タイプを定義する必要があるかもしれません。キャストを作成するには、`make:cast` Artisan コマンドを実行します。新しいキャスト クラスは、`app/Casts` ディレクトリに配置されます。

```shell
php artisan make:cast Json
```

すべてのカスタム キャスト クラスは、`CastsAttributes` インターフェイスを実装します。このインターフェイスを実装するクラスは、`get` メソッドと `set` メソッドを定義する必要があります。 `get` メソッドはデータベースからの生の値をキャスト値に変換する役割を果たしますが、`set` メソッドはキャスト値をデータベースに保存できる生の値に変換する必要があります。例として、組み込みの `json` キャスト タイプをカスタム キャスト タイプとして再実装します。

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Json implements CastsAttributes
    {
        /**
         * Cast the given value.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  mixed  $value
         * @param  array  $attributes
         * @return array
         */
        public function get($model, $key, $value, $attributes)
        {
            return json_decode($value, true);
        }

        /**
         * Prepare the given value for storage.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  array  $value
         * @param  array  $attributes
         * @return string
         */
        public function set($model, $key, $value, $attributes)
        {
            return json_encode($value);
        }
    }

カスタム キャスト タイプを定義したら、そのクラス名を使用してそれをモデル属性にアタッチできます。

    <?php

    namespace App\Models;

    use App\Casts\Json;
    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * The attributes that should be cast.
         *
         * @var array
         */
        protected $casts = [
            'options' => Json::class,
        ];
    }

<a name="value-object-casting"></a>
### 値オブジェクトのキャスト

値をプリミティブ型にキャストすることに限定されません。値をオブジェクトにキャストすることもできます。値をオブジェクトにキャストするカスタム キャストの定義は、プリミティブ型へのキャストと非常に似ています。ただし、`set` メソッドは、モデルに保存可能な生の値を設定するために使用されるキーと値のペアの配列を返す必要があります。

例として、複数のモデル値を単一の `Address` 値オブジェクトにキャストするカスタム キャスト クラスを定義します。 `Address` 値には、`lineOne` と `lineTwo` という 2 つのパブリック プロパティがあると仮定します。

    <?php

    namespace App\Casts;

    use App\ValueObjects\Address as AddressValueObject;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
    use InvalidArgumentException;

    class Address implements CastsAttributes
    {
        /**
         * Cast the given value.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  mixed  $value
         * @param  array  $attributes
         * @return \App\ValueObjects\Address
         */
        public function get($model, $key, $value, $attributes)
        {
            return new AddressValueObject(
                $attributes['address_line_one'],
                $attributes['address_line_two']
            );
        }

        /**
         * Prepare the given value for storage.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  \App\ValueObjects\Address  $value
         * @param  array  $attributes
         * @return array
         */
        public function set($model, $key, $value, $attributes)
        {
            if (! $value instanceof AddressValueObject) {
                throw new InvalidArgumentException('The given value is not an Address instance.');
            }

            return [
                'address_line_one' => $value->lineOne,
                'address_line_two' => $value->lineTwo,
            ];
        }
    }

値オブジェクトにキャストする場合、値オブジェクトに加えられた変更は、モデルが保存される前に自動的にモデルに同期されます。

    use App\Models\User;

    $user = User::find(1);

    $user->address->lineOne = 'Updated Address Value';

    $user->save();

> **注記**
> 値オブジェクトを含む Eloquent モデルを JSON または配列にシリアル化する予定がある場合は、値オブジェクトに `Illuminate\Contracts\Support\Arrayable` インターフェイスと `JsonSerializable` インターフェイスを実装する必要があります。

<a name="array-json-serialization"></a>
### 配列/JSONシリアル化

Eloquent モデルが `toArray` および `toJson` メソッドを使用して配列または JSON に変換される場合、カスタム キャスト値オブジェクトは、`Illuminate\Contracts\Support\Arrayable` および `JsonSerializable` インターフェイスを実装している限り、通常はシリアル化されます。ただし、サードパーティのライブラリによって提供される値オブジェクトを使用する場合、これらのインターフェイスをオブジェクトに追加できない場合があります。

したがって、カスタム キャスト クラスが値オブジェクトのシリアル化を担当するように指定できます。これを行うには、カスタム キャスト クラスで `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` インターフェイスを実装する必要があります。このインターフェイスは、クラスに値オブジェクトのシリアル化された形式を返す `serialize` メソッドを含める必要があることを示しています。

    /**
     * Get the serialized representation of the value.
     *
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @param  string  $key
     * @param  mixed  $value
     * @param  array  $attributes
     * @return mixed
     */
    public function serialize($model, string $key, $value, array $attributes)
    {
        return (string) $value;
    }

<a name="inbound-casting"></a>
### インバウンドキャスト

場合によっては、モデルに設定されている値を変換するだけで、モデルから属性を取得するときに操作を実行しないカスタム キャスト クラスの作成が必要になる場合があります。

インバウンドのみのカスタム キャストは、`CastsInboundAttributes` インターフェイスを実装する必要があります。これには、`set` メソッドの定義のみが必要です。 `make:cast` Artisan コマンドは、`--inbound` オプションを指定して呼び出して、インバウンド専用のキャスト クラスを生成できます。

```shell
php artisan make:cast Hash --inbound
```

インバウンド専用キャストの典型的な例は、「ハッシュ」キャストです。たとえば、指定されたアルゴリズムを介して受信値をハッシュするキャストを定義できます。

    <?php

    namespace App\Casts;

    use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;

    class Hash implements CastsInboundAttributes
    {
        /**
         * The hashing algorithm.
         *
         * @var string
         */
        protected $algorithm;

        /**
         * Create a new cast class instance.
         *
         * @param  string|null  $algorithm
         * @return void
         */
        public function __construct($algorithm = null)
        {
            $this->algorithm = $algorithm;
        }

        /**
         * Prepare the given value for storage.
         *
         * @param  \Illuminate\Database\Eloquent\Model  $model
         * @param  string  $key
         * @param  array  $value
         * @param  array  $attributes
         * @return string
         */
        public function set($model, $key, $value, $attributes)
        {
            return is_null($this->algorithm)
                        ? bcrypt($value)
                        : hash($this->algorithm, $value);
        }
    }

<a name="cast-parameters"></a>
### キャストパラメータ

カスタム キャストをモデルにアタッチする場合、`:` 文字を使用してクラス名からキャスト パラメータを分離し、複数のパラメータをカンマで区切ることでキャスト パラメータを指定できます。パラメータはキャスト クラスのコンストラクターに渡されます。

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'secret' => Hash::class.':sha256',
    ];

<a name="castables"></a>
### キャスタブル

アプリケーションの値オブジェクトが独自のカスタム キャスト クラスを定義できるようにしたい場合があります。カスタム キャスト クラスをモデルにアタッチする代わりに、`Illuminate\Contracts\Database\Eloquent\Castable` インターフェイスを実装する値オブジェクト クラスをアタッチすることもできます。

    use App\Models\Address;

    protected $casts = [
        'address' => Address::class,
    ];

`Castable` インターフェイスを実装するオブジェクトは、`Castable` クラスとのキャストを担当するカスタム キャスタ クラスのクラス名を返す `castUsing` メソッドを定義する必要があります。

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use App\Casts\Address as AddressCast;

    class Address implements Castable
    {
        /**
         * Get the name of the caster class to use when casting from / to this cast target.
         *
         * @param  array  $arguments
         * @return string
         */
        public static function castUsing(array $arguments)
        {
            return AddressCast::class;
        }
    }

`Castable` クラスを使用する場合でも、`$casts` 定義に引数を指定できます。引数は `castUsing` メソッドに渡されます。

    use App\Models\Address;

    protected $casts = [
        'address' => Address::class.':argument',
    ];

<a name="anonymous-cast-classes"></a>
#### キャスタブルと匿名キャスト クラス

「キャスト可能」を PHP の [匿名クラス](https://www.php.net/manual/en/language.oop5.anonymous.php) と組み合わせることで、値オブジェクトとそのキャスト ロジックを単一のキャスト可能オブジェクトとして定義できます。これを実現するには、値オブジェクトの `castUsing` メソッドから匿名クラスを返します。匿名クラスは、`CastsAttributes` インターフェイスを実装する必要があります。

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Database\Eloquent\Castable;
    use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

    class Address implements Castable
    {
        // ...

        /**
         * Get the caster class to use when casting from / to this cast target.
         *
         * @param  array  $arguments
         * @return object|string
         */
        public static function castUsing(array $arguments)
        {
            return new class implements CastsAttributes
            {
                public function get($model, $key, $value, $attributes)
                {
                    return new Address(
                        $attributes['address_line_one'],
                        $attributes['address_line_two']
                    );
                }

                public function set($model, $key, $value, $attributes)
                {
                    return [
                        'address_line_one' => $value->lineOne,
                        'address_line_two' => $value->lineTwo,
                    ];
                }
            };
        }
    }

