<!-- # Eloquent: Mutators & Casting -->
# Eloquent: Mutators & Casting

- [Introduction](#introduction)
- [Accessors & Mutators](#accessors-and-mutators)
    - [Defining An Accessor](#defining-an-accessor)
    - [Defining A Mutator](#defining-a-mutator)
- [Attribute Casting](#attribute-casting)
    - [Array & JSON Casting](#array-and-json-casting)
    - [Date Casting](#date-casting)
    - [Enum Casting](#enum-casting)
    - [Encrypted Casting](#encrypted-casting)
    - [Query Time Casting](#query-time-casting)
- [Custom Casts](#custom-casts)
    - [Value Object Casting](#value-object-casting)
    - [Array / JSON Serialization](#array-json-serialization)
    - [Inbound Casting](#inbound-casting)
    - [Cast Parameters](#cast-parameters)
    - [Castables](#castables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/9.x/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model. -->
accessor、mutator、およびattribute castingを使用すると、Eloquent 属性値をモデル インスタンスで取得または設定するときに、その値を変換できます。たとえば、[Laravel encrypter](/docs/9.x/encryption) を使用して、データベースに保存されている値を暗号化し、Eloquent モデルでアクセスするときにその属性を自動的に復号化することができます。または、Eloquent モデル経由でアクセスするときに、データベースに保存されている JSON 文字列を配列に変換することもできます。

<a name="accessors-and-mutators"></a>
<!-- ## Accessors & Mutators -->
## Accessors & Mutators

<a name="defining-an-accessor"></a>
<!-- ### Defining An Accessor -->
### Defining An Accessor

<!-- An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a protected method on your model to represent the accessible attribute. This method name should correspond to the "camel case" representation of the true underlying model attribute / database column when applicable. -->
accessorは、アクセス時に Eloquent 属性値を変換します。accessorを定義するには、アクセス可能な属性を表す保護されたメソッドをモデル上に作成します。このメソッド名は、該当する場合、実際の基になるモデル属性/データベース列の「キャメル ケース」表現に対応する必要があります。

<!-- In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute. All attribute accessor / mutator methods must declare a return type-hint of `Illuminate\Database\Eloquent\Casts\Attribute`: -->
この例では、`first_name` 属性のaccessorを定義します。accessorは、`first_name` 属性の値を取得しようとすると、Eloquent によって自動的に呼び出されます。すべての属性accessor/mutator メソッドは、戻り値の型ヒント `Illuminate\Database\Eloquent\Casts\Attribute` を宣言する必要があります。

```
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
```

<!-- All accessor methods return an `Attribute` instance which defines how the attribute will be accessed and, optionally, mutated. In this example, we are only defining how the attribute will be accessed. To do so, we supply the `get` argument to the `Attribute` class constructor. -->
すべてのaccessor メソッドは、属性へのアクセス方法と、オプションで変更する方法を定義する `Attribute` インスタンスを返します。この例では、属性にアクセスする方法のみを定義しています。これを行うには、`get` 引数を `Attribute` クラス コンストラクターに指定します。

<!-- As you can see, the original value of the column is passed to the accessor, allowing you to manipulate and return the value. To access the value of the accessor, you may simply access the `first_name` attribute on a model instance: -->
ご覧のとおり、列の元の値がaccessorに渡されるため、値を操作して返すことができます。accessorの値にアクセスするには、モデル インスタンスの `first_name` 属性にアクセスするだけです。

```
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```

> [!NOTE]
> これらの計算値をモデルの配列/JSON 表現に追加したい場合は、[you will need to append them](/docs/9.x/eloquent-serialization#appending-values-to-json)。

<a name="building-value-objects-from-multiple-attributes"></a>
<!-- #### Building Value Objects From Multiple Attributes -->
#### Building Value Objects From Multiple Attributes

<!-- Sometimes your accessor may need to transform multiple model attributes into a single "value object". To do so, your `get` closure may accept a second argument of `$attributes`, which will be automatically supplied to the closure and will contain an array of all of the model's current attributes: -->
場合によっては、accessorが複数のモデル属性を 1 つの「値オブジェクト」に変換する必要がある場合があります。これを行うには、`get` クロージャーは `$attributes` の 2 番目の引数を受け入れることができます。これは自動的にクロージャーに提供され、モデルの現在の属性すべての配列が含まれます。

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
<!-- #### Accessor Caching -->
#### Accessor Caching

<!-- When returning value objects from accessors, any changes made to the value object will automatically be synced back to the model before the model is saved. This is possible because Eloquent retains instances returned by accessors so it can return the same instance each time the accessor is invoked: -->
accessorから値オブジェクトを返す場合、値オブジェクトに加えられた変更は、モデルが保存される前に自動的にモデルに同期されます。これが可能なのは、Eloquent がaccessorによって返されたインスタンスを保持し、accessorが呼び出されるたびに同じインスタンスを返すことができるためです。

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```

<!-- However, you may sometimes wish to enable caching for primitive values like strings and booleans, particularly if they are computationally intensive. To accomplish this, you may invoke the `shouldCache` method when defining your accessor: -->
ただし、特に計算負荷が高い場合、文字列やブール値などのプリミティブ値のキャッシュを有効にしたい場合があります。これを実現するには、accessorを定義するときに `shouldCache` メソッドを呼び出します。

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn ($value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```

<!-- If you would like to disable the object caching behavior of attributes, you may invoke the `withoutObjectCaching` method when defining the attribute: -->
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
<!-- ### Defining A Mutator -->
### Defining A Mutator

<!-- A mutator transforms an Eloquent attribute value when it is set. To define a mutator, you may provide the `set` argument when defining your attribute. Let's define a mutator for the `first_name` attribute. This mutator will be automatically called when we attempt to set the value of the `first_name` attribute on the model: -->
mutatorは、Eloquent 属性値が設定されているときにそれを変換します。mutatorを定義するには、属性を定義するときに `set` 引数を指定できます。 `first_name` 属性のmutatorを定義しましょう。このmutatorは、モデルに `first_name` 属性の値を設定しようとすると自動的に呼び出されます。

```
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
```

<!-- The mutator closure will receive the value that is being set on the attribute, allowing you to manipulate the value and return the manipulated value. To use our mutator, we only need to set the `first_name` attribute on an Eloquent model: -->
mutator クロージャーは属性に設定されている値を受け取り、値を操作して操作された値を返すことができます。mutatorを使用するには、Eloquent モデルで `first_name` 属性を設定するだけです。

```
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```

<!-- In this example, the `set` callback will be called with the value `Sally`. The mutator will then apply the `strtolower` function to the name and set its resulting value in the model's internal `$attributes` array. -->
この例では、`set` コールバックが値 `Sally` で呼び出されます。次に、mutatorは `strtolower` 関数を名前に適用し、その結果の値をモデルの内部 `$attributes` 配列に設定します。

<a name="mutating-multiple-attributes"></a>
<!-- #### Mutating Multiple Attributes -->
#### Mutating Multiple Attributes

<!-- Sometimes your mutator may need to set multiple attributes on the underlying model. To do so, you may return an array from the `set` closure. Each key in the array should correspond with an underlying attribute / database column associated with the model: -->
mutatorは、基礎となるモデルに複数の属性を設定する必要がある場合があります。これを行うには、`set` クロージャから配列を返すことができます。配列内の各キーは、モデルに関連付けられた基になる属性/データベース列に対応する必要があります。

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
<!-- ## Attribute Casting -->
## Attribute Casting

<!-- Attribute casting provides functionality similar to accessors and mutators without requiring you to define any additional methods on your model. Instead, your model's `$casts` property provides a convenient method of converting attributes to common data types. -->
attribute castingは、モデルに追加のメソッドを定義する必要なく、accessorやmutatorと同様の機能を提供します。代わりに、モデルの `$casts` プロパティは、属性を一般的なデータ型に変換する便利な方法を提供します。

<!-- The `$casts` property should be an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are: -->
`$casts` プロパティは、キーがcastされる属性の名前、値が列をcastする型である配列である必要があります。サポートされているcast タイプは次のとおりです。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
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
-->
- `array`
- `AsStringable::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
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

<!-- </div> -->
</div>

<!-- To demonstrate attribute casting, let's cast the `is_admin` attribute, which is stored in our database as an integer (`0` or `1`) to a boolean value: -->
属性のcastを示すために、データベースに整数 (`0` または `1`) として保存されている `is_admin` 属性をブール値にcastしてみましょう。

```
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
```

<!-- After defining the cast, the `is_admin` attribute will always be cast to a boolean when you access it, even if the underlying value is stored in the database as an integer: -->
castを定義した後、基になる値がデータベースに整数として格納されている場合でも、アクセス時に `is_admin` 属性は常にブール値にcastされます。

```
$user = App\Models\User::find(1);

if ($user->is_admin) {
    //
}
```

<!-- If you need to add a new, temporary cast at runtime, you may use the `mergeCasts` method. These cast definitions will be added to any of the casts already defined on the model: -->
実行時に新しい一時的なcastを追加する必要がある場合は、`mergeCasts` メソッドを使用できます。これらのcast定義は、モデルですでに定義されているcastのいずれかに追加されます。

```
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```

> [!WARNING]
> `null` の属性はcastされません。さらに、リレーションシップと同じ名前のcast (または属性) を定義しないでください。

<a name="stringable-casting"></a>
<!-- #### Stringable Casting -->
#### Stringable Casting

<!-- You may use the `Illuminate\Database\Eloquent\Casts\AsStringable` cast class to cast a model attribute to a [fluent `Illuminate\Support\Stringable` object](/docs/9.x/helpers#fluent-strings-method-list): -->
`Illuminate\Database\Eloquent\Casts\AsStringable` cast クラスを使用して、モデル属性を [fluent `Illuminate\Support\Stringable` object](/docs/9.x/helpers#fluent-strings-method-list) にcastできます。

```
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
```

<a name="array-and-json-casting"></a>
<!-- ### Array & JSON Casting -->
### Array & JSON Casting

<!-- The `array` cast is particularly useful when working with columns that are stored as serialized JSON. For example, if your database has a `JSON` or `TEXT` field type that contains serialized JSON, adding the `array` cast to that attribute will automatically deserialize the attribute to a PHP array when you access it on your Eloquent model: -->
`array` castは、シリアル化された JSON として保存されている列を操作する場合に特に便利です。たとえば、データベースにシリアル化された JSON を含む `JSON` または `TEXT` フィールド タイプがある場合、その属性に `array` castを追加すると、Eloquent モデルでアクセスするときに属性が PHP 配列に自動的に逆シリアル化されます。

```
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
```

<!-- Once the cast is defined, you may access the `options` attribute and it will automatically be deserialized from JSON into a PHP array. When you set the value of the `options` attribute, the given array will automatically be serialized back into JSON for storage: -->
castが定義されたら、`options` 属性にアクセスすると、JSON から PHP 配列に自動的に逆シリアル化されます。 `options` 属性の値を設定すると、指定された配列が自動的にシリアル化されて JSON に戻され、保存されます。

```
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```

<!-- To update a single field of a JSON attribute with a more terse syntax, you may use the `->` operator when calling the `update` method: -->
JSON 属性の単一フィールドをより簡潔な構文で更新するには、`update` メソッドを呼び出すときに `->` 演算子を使用できます。

```
$user = User::find(1);

$user->update(['options->key' => 'value']);
```

<a name="array-object-and-collection-casting"></a>
<!-- #### Array Object & Collection Casting -->
#### Array Object & Collection Casting

<!-- Although the standard `array` cast is sufficient for many applications, it does have some disadvantages. Since the `array` cast returns a primitive type, it is not possible to mutate an offset of the array directly. For example, the following code will trigger a PHP error: -->
標準の `array` castは多くのアプリケーションには十分ですが、いくつかの欠点があります。 `array` castはプリミティブ型を返すため、配列のオフセットを直接変更することはできません。たとえば、次のコードは PHP エラーをトリガーします。

```
$user = User::find(1);

$user->options['key'] = $value;
```

<!-- To solve this, Laravel offers an `AsArrayObject` cast that casts your JSON attribute to an [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) class. This feature is implemented using Laravel's [custom cast](#custom-casts) implementation, which allows Laravel to intelligently cache and transform the mutated object such that individual offsets may be modified without triggering a PHP error. To use the `AsArrayObject` cast, simply assign it to an attribute: -->
これを解決するために、Laravel は JSON 属性を [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) クラスにcastする `AsArrayObject` castを提供します。この機能は、Laravel の [custom cast](#custom-casts) 実装を使用して実装されます。これにより、Laravel は、PHP エラーを引き起こすことなく個々のオフセットを変更できるように、変更されたオブジェクトをインテリジェントにキャッシュおよび変換できます。 `AsArrayObject` castを使用するには、それを属性に割り当てるだけです。

```
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'options' => AsArrayObject::class,
];
```

<!-- Similarly, Laravel offers an `AsCollection` cast that casts your JSON attribute to a Laravel [Collection](/docs/9.x/collections) instance: -->
同様に、Laravel は、JSON 属性を Laravel [Collection](/docs/9.x/collections) インスタンスにcastする `AsCollection` castを提供します。

```
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'options' => AsCollection::class,
];
```

<a name="date-casting"></a>
<!-- ### Date Casting -->
### Date Casting

<!-- By default, Eloquent will cast the `created_at` and `updated_at` columns to instances of [Carbon](https://github.com/briannesbitt/Carbon), which extends the PHP `DateTime` class and provides an assortment of helpful methods. You may cast additional date attributes by defining additional date casts within your model's `$casts` property array. Typically, dates should be cast using the `datetime` or `immutable_datetime` cast types. -->
デフォルトでは、Eloquent は `created_at` 列と `updated_at` 列を [Carbon](https://github.com/briannesbitt/Carbon) のインスタンスにcastします。これは、PHP `DateTime` クラスを拡張し、さまざまな便利なメソッドを提供します。モデルの `$casts` プロパティ配列内で追加の日付castを定義することで、追加の日付属性をcastできます。通常、日付は `datetime` または `immutable_datetime` cast タイプを使用してcastする必要があります。

<!-- When defining a `date` or `datetime` cast, you may also specify the date's format. This format will be used when the [model is serialized to an array or JSON](/docs/9.x/eloquent-serialization): -->
`date` または `datetime` castを定義するときは、日付の形式も指定できます。この形式は、[model is serialized to an array or JSON](/docs/9.x/eloquent-serialization) の場合に使用されます。

```
/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'created_at' => 'datetime:Y-m-d',
];
```

<!-- When a column is cast as a date, you may set the corresponding model attribute value to a UNIX timestamp, date string (`Y-m-d`), date-time string, or a `DateTime` / `Carbon` instance. The date's value will be correctly converted and stored in your database. -->
列が日付としてcastされる場合、対応するモデル属性値を UNIX タイムスタンプ、日付文字列（`Y-m-d`）、日時文字列、または `DateTime` / `Carbon` インスタンスに設定できます。日付の値は正しく変換され、データベースに保存されます。

<!-- You may customize the default serialization format for all of your model's dates by defining a `serializeDate` method on your model. This method does not affect how your dates are formatted for storage in the database: -->
モデルで `serializeDate` メソッドを定義することで、モデルのすべての日付のデフォルトのシリアル化形式をカスタマイズできます。この方法は、データベースに保存する際の日付の形式には影響しません。

```
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
```

<!-- To specify the format that should be used when actually storing a model's dates within your database, you should define a `$dateFormat` property on your model: -->
実際にモデルの日付をデータベース内に保存するときに使用する形式を指定するには、モデルで `$dateFormat` プロパティを定義する必要があります。

```
/**
 * The storage format of the model's date columns.
 *
 * @var string
 */
protected $dateFormat = 'U';
```

<a name="date-casting-and-timezones"></a>
<!-- #### Date Casting, Serialization, & Timezones -->
#### Date Casting, Serialization, & Timezones

<!-- By default, the `date` and `datetime` casts will serialize dates to a UTC ISO-8601 date string (`1986-05-28T21:05:54.000000Z`), regardless of the timezone specified in your application's `timezone` configuration option. You are strongly encouraged to always use this serialization format, as well as to store your application's dates in the UTC timezone by not changing your application's `timezone` configuration option from its default `UTC` value. Consistently using the UTC timezone throughout your application will provide the maximum level of interoperability with other date manipulation libraries written in PHP and JavaScript. -->
デフォルトでは、`date` および `datetime` castは、アプリケーションの `timezone` 構成オプションで指定されたタイムゾーンに関係なく、日付を UTC ISO-8601 日付文字列 (`1986-05-28T21:05:54.000000Z`) にシリアル化します。常にこのシリアル化形式を使用し、アプリケーションの `timezone` 構成オプションをデフォルトの `UTC` 値から変更せず、アプリケーションの日付を UTC タイムゾーンで保存することを強くお勧めします。アプリケーション全体で一貫して UTC タイムゾーンを使用すると、PHP および JavaScript で作成された他の日付操作ライブラリとの相互運用性が最大レベルで提供されます。

<!-- If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. -->
`datetime:Y-m-d H:i:s` などのカスタム形式が `date` または `datetime` castに適用される場合、日付のシリアル化中に Carbon インスタンスの内部タイムゾーンが使用されます。通常、これはアプリケーションの `timezone` 構成オプションで指定されたタイムゾーンになります。

<a name="enum-casting"></a>
<!-- ### Enum Casting -->
### Enum Casting

> [!WARNING]
> Enum castは PHP 8.1 以降でのみ使用できます。

<!-- Eloquent also allows you to cast your attribute values to PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `$casts` property array: -->
Eloquent では、属性値を PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php) にcastすることもできます。これを実現するには、モデルの `$casts` プロパティ配列にcastする属性と列挙型を指定します。

```
use App\Enums\ServerStatus;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

<!-- Once you have defined the cast on your model, the specified attribute will be automatically cast to and from an enum when you interact with the attribute: -->
モデルでcastを定義すると、指定した属性は、属性を操作するときに列挙型との間で自動的にcastされます。

```
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="casting-arrays-of-enums"></a>
<!-- #### Casting Arrays Of Enums -->
#### Casting Arrays Of Enums

<!-- Sometimes you may need your model to store an array of enum values within a single column. To accomplish this, you may utilize the `AsEnumArrayObject` or `AsEnumCollection` casts provided by Laravel: -->
場合によっては、モデルで列挙値の配列を 1 つの列に格納する必要がある場合があります。これを実現するには、Laravel が提供する `AsEnumArrayObject` または `AsEnumCollection` castを利用できます。

```
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
```

<a name="encrypted-casting"></a>
<!-- ### Encrypted Casting -->
### Encrypted Casting

<!-- The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/9.x/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database. -->
`encrypted` castは、Laravel の組み込み [encryption](/docs/9.x/encryption) 機能を使用してモデルの属性値を暗号化します。さらに、`encrypted:array`、`encrypted:collection`、`encrypted:object`、`AsEncryptedArrayObject`、および `AsEncryptedCollection` castは、暗号化されていないcastと同様に機能します。ただし、ご想像のとおり、基になる値はデータベースに保存されるときに暗号化されます。

<!-- As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values. -->
暗号化されたテキストの最終的な長さは予測できず、対応する平文よりも長いため、関連するデータベース列が `TEXT` 型以上であることを確認してください。さらに、値はデータベース内で暗号化されるため、暗号化された属性値をクエリまたは検索することはできません。

<a name="key-rotation"></a>
<!-- #### Key Rotation -->
#### Key Rotation

<!-- As you may know, Laravel encrypts strings using the `key` configuration value specified in your application's `app` configuration file. Typically, this value corresponds to the value of the `APP_KEY` environment variable. If you need to rotate your application's encryption key, you will need to manually re-encrypt your encrypted attributes using the new key. -->
ご存知のとおり、Laravel は、アプリケーションの `app` 構成ファイルで指定された `key` 構成値を使用して文字列を暗号化します。通常、この値は `APP_KEY` 環境変数の値に対応します。アプリケーションの暗号化キーをローテーションする必要がある場合は、新しいキーを使用して暗号化された属性を手動で再暗号化する必要があります。

<a name="query-time-casting"></a>
<!-- ### Query Time Casting -->
### Query Time Casting

<!-- Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query: -->
テーブルから生の値を選択する場合など、クエリの実行中にcastの適用が必要になる場合があります。たとえば、次のクエリについて考えてみましょう。

```
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->get();
```

<!-- The `last_posted_at` attribute on the results of this query will be a simple string. It would be wonderful if we could apply a `datetime` cast to this attribute when executing the query. Thankfully, we may accomplish this using the `withCasts` method: -->
このクエリの結果の `last_posted_at` 属性は単純な文字列になります。クエリの実行時にこの属性に `datetime` castを適用できれば素晴らしいでしょう。ありがたいことに、`withCasts` メソッドを使用してこれを実現できます。

```
$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
            ->whereColumn('user_id', 'users.id')
])->withCasts([
    'last_posted_at' => 'datetime'
])->get();
```

<a name="custom-casts"></a>
<!-- ## Custom Casts -->
## Custom Casts

<!-- Laravel has a variety of built-in, helpful cast types; however, you may occasionally need to define your own cast types. To create a cast, execute the `make:cast` Artisan command. The new cast class will be placed in your `app/Casts` directory: -->
Laravel には、さまざまな便利なcast型が組み込まれています。ただし、場合によっては、独自のcast タイプを定義する必要があるかもしれません。castを作成するには、`make:cast` Artisan コマンドを実行します。新しいcast クラスは、`app/Casts` ディレクトリに配置されます。

```shell
php artisan make:cast Json
```

<!-- All custom cast classes implement the `CastsAttributes` interface. Classes that implement this interface must define a `get` and `set` method. The `get` method is responsible for transforming a raw value from the database into a cast value, while the `set` method should transform a cast value into a raw value that can be stored in the database. As an example, we will re-implement the built-in `json` cast type as a custom cast type: -->
すべてのカスタム cast クラスは、`CastsAttributes` インターフェイスを実装します。このインターフェイスを実装するクラスは、`get` メソッドと `set` メソッドを定義する必要があります。 `get` メソッドはデータベースからの生の値をcast値に変換する役割を果たしますが、`set` メソッドはcast値をデータベースに保存できる生の値に変換する必要があります。例として、組み込みの `json` cast タイプをカスタム cast タイプとして再実装します。

```
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
```

<!-- Once you have defined a custom cast type, you may attach it to a model attribute using its class name: -->
カスタム cast タイプを定義したら、そのクラス名を使用してそれをモデル属性にアタッチできます。

```
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
```

<a name="value-object-casting"></a>
<!-- ### Value Object Casting -->
### Value Object Casting

<!-- You are not limited to casting values to primitive types. You may also cast values to objects. Defining custom casts that cast values to objects is very similar to casting to primitive types; however, the `set` method should return an array of key / value pairs that will be used to set raw, storable values on the model. -->
値をプリミティブ型にcastすることに限定されません。値をオブジェクトにcastすることもできます。値をオブジェクトにcastするカスタム castの定義は、プリミティブ型へのcastと非常に似ています。ただし、`set` メソッドは、モデルに保存可能な生の値を設定するために使用されるキーと値のペアの配列を返す必要があります。

<!-- As an example, we will define a custom cast class that casts multiple model values into a single `Address` value object. We will assume the `Address` value has two public properties: `lineOne` and `lineTwo`: -->
例として、複数のモデル値を単一の `Address` 値オブジェクトにcastするカスタム cast クラスを定義します。 `Address` 値には、`lineOne` と `lineTwo` という 2 つのパブリック プロパティがあると仮定します。

```
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
```

<!-- When casting to value objects, any changes made to the value object will automatically be synced back to the model before the model is saved: -->
値オブジェクトにcastする場合、値オブジェクトに加えられた変更は、モデルが保存される前に自動的にモデルに同期されます。

```
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```

> [!NOTE]
> 値オブジェクトを含む Eloquent モデルを JSON または配列にシリアル化する予定がある場合は、値オブジェクトに `Illuminate\Contracts\Support\Arrayable` インターフェイスと `JsonSerializable` インターフェイスを実装する必要があります。

<a name="array-json-serialization"></a>
<!-- ### Array / JSON Serialization -->
### Array / JSON Serialization

<!-- When an Eloquent model is converted to an array or JSON using the `toArray` and `toJson` methods, your custom cast value objects will typically be serialized as well as long as they implement the `Illuminate\Contracts\Support\Arrayable` and `JsonSerializable` interfaces. However, when using value objects provided by third-party libraries, you may not have the ability to add these interfaces to the object. -->
Eloquent モデルが `toArray` および `toJson` メソッドを使用して配列または JSON に変換される場合、カスタム cast値オブジェクトは、`Illuminate\Contracts\Support\Arrayable` および `JsonSerializable` インターフェイスを実装している限り、通常はシリアル化されます。ただし、サードパーティのライブラリによって提供される値オブジェクトを使用する場合、これらのインターフェイスをオブジェクトに追加できない場合があります。

<!-- Therefore, you may specify that your custom cast class will be responsible for serializing the value object. To do so, your custom cast class should implement the `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` interface. This interface states that your class should contain a `serialize` method which should return the serialized form of your value object: -->
したがって、カスタム cast クラスが値オブジェクトのシリアル化を担当するように指定できます。これを行うには、カスタム cast クラスで `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` インターフェイスを実装する必要があります。このインターフェイスは、クラスに値オブジェクトのシリアル化された形式を返す `serialize` メソッドを含める必要があることを示しています。

```
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
```

<a name="inbound-casting"></a>
<!-- ### Inbound Casting -->
### Inbound Casting

<!-- Occasionally, you may need to write a custom cast class that only transforms values that are being set on the model and does not perform any operations when attributes are being retrieved from the model. -->
場合によっては、モデルに設定されている値を変換するだけで、モデルから属性を取得するときに操作を実行しないカスタム cast クラスの作成が必要になる場合があります。

<!-- Inbound only custom casts should implement the `CastsInboundAttributes` interface, which only requires a `set` method to be defined. The `make:cast` Artisan command may be invoked with the `--inbound` option to generate an inbound only cast class: -->
インバウンドのみのカスタム castは、`CastsInboundAttributes` インターフェイスを実装する必要があります。これには、`set` メソッドの定義のみが必要です。 `make:cast` Artisan コマンドは、`--inbound` オプションを指定して呼び出して、インバウンド専用のcast クラスを生成できます。

```shell
php artisan make:cast Hash --inbound
```

<!-- A classic example of an inbound only cast is a "hashing" cast. For example, we may define a cast that hashes inbound values via a given algorithm: -->
インバウンド専用castの典型的な例は、「ハッシュ」castです。たとえば、指定されたアルゴリズムを介して受信値をハッシュするcastを定義できます。

```
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
```

<a name="cast-parameters"></a>
<!-- ### Cast Parameters -->
### Cast Parameters

<!-- When attaching a custom cast to a model, cast parameters may be specified by separating them from the class name using a `:` character and comma-delimiting multiple parameters. The parameters will be passed to the constructor of the cast class: -->
カスタム castをモデルにアタッチする場合、`:` 文字を使用してクラス名からcast パラメータを分離し、複数のパラメータをカンマで区切ることでcast パラメータを指定できます。パラメータはcast クラスのコンストラクターに渡されます。

```
/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'secret' => Hash::class.':sha256',
];
```

<a name="castables"></a>
<!-- ### Castables -->
### Castables

<!-- You may want to allow your application's value objects to define their own custom cast classes. Instead of attaching the custom cast class to your model, you may alternatively attach a value object class that implements the `Illuminate\Contracts\Database\Eloquent\Castable` interface: -->
アプリケーションの値オブジェクトが独自のカスタム cast クラスを定義できるようにしたい場合があります。カスタム cast クラスをモデルにアタッチする代わりに、`Illuminate\Contracts\Database\Eloquent\Castable` インターフェイスを実装する値オブジェクト クラスをアタッチすることもできます。

```
use App\Models\Address;

protected $casts = [
    'address' => Address::class,
];
```

<!-- Objects that implement the `Castable` interface must define a `castUsing` method that returns the class name of the custom caster class that is responsible for casting to and from the `Castable` class: -->
`Castable` インターフェイスを実装するオブジェクトは、`Castable` クラスとのcastを担当するカスタム caster クラスのクラス名を返す `castUsing` メソッドを定義する必要があります。

```
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
```

<!-- When using `Castable` classes, you may still provide arguments in the `$casts` definition. The arguments will be passed to the `castUsing` method: -->
`Castable` クラスを使用する場合でも、`$casts` 定義に引数を指定できます。引数は `castUsing` メソッドに渡されます。

```
use App\Models\Address;

protected $casts = [
    'address' => Address::class.':argument',
];
```

<a name="anonymous-cast-classes"></a>
<!-- #### Castables & Anonymous Cast Classes -->
#### Castables & Anonymous Cast Classes

<!-- By combining "castables" with PHP's [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php), you may define a value object and its casting logic as a single castable object. To accomplish this, return an anonymous class from your value object's `castUsing` method. The anonymous class should implement the `CastsAttributes` interface: -->
「Castable」を PHP の [anonymous classes](https://www.php.net/manual/en/language.oop5.anonymous.php) と組み合わせることで、値オブジェクトとそのcast ロジックを単一のCastableオブジェクトとして定義できます。これを実現するには、値オブジェクトの `castUsing` メソッドから匿名クラスを返します。匿名クラスは、`CastsAttributes` インターフェイスを実装する必要があります。

```
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
```

