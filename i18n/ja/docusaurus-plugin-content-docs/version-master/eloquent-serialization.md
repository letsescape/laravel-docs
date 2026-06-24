<!-- # Eloquent: Serialization -->
# Eloquent: Serialization

- [Introduction](#introduction)
- [Serializing Models and Collections](#serializing-models-and-collections)
    - [Serializing to Arrays](#serializing-to-arrays)
    - [Serializing to JSON](#serializing-to-json)
- [Hiding Attributes From JSON](#hiding-attributes-from-json)
- [Appending Values to JSON](#appending-values-to-json)
- [Date Serialization](#date-serialization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When building APIs using Laravel, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in the serialized representation of your models. -->
Laravel を使用して API を構築する場合、多くの場合、モデルと関係を配列または JSON に変換する必要があります。 Eloquent には、これらの変換を行うだけでなく、モデルのシリアル化された表現にどの属性を含めるかを制御するための便利なメソッドが含まれています。

> [!NOTE]
> Eloquent モデルとコレクションの JSON シリアル化を処理するさらに堅牢な方法については、[Eloquent API resources](/docs/master/eloquent-resources) のドキュメントを確認してください。

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models and Collections -->
## Serializing Models and Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing to Arrays -->
### Serializing to Arrays

<!-- To convert a model and its loaded [relationships](/docs/master/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
モデルとそのロードされた [relationships](/docs/master/eloquent-relationships) を配列に変換するには、`toArray` メソッドを使用する必要があります。このメソッドは再帰的であるため、すべての属性とすべての関係 (関係の関係を含む) が配列に変換されます。

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` メソッドは、モデルの属性を配列に変換するために使用できますが、その関係は変換できません。

```php
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/master/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
コレクション インスタンスで `toArray` メソッドを呼び出して、モデルの [collections](/docs/master/eloquent-collections) 全体を配列に変換することもできます。

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing to JSON -->
### Serializing to JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
モデルを JSON に変換するには、`toJson` メソッドを使用する必要があります。 `toArray` と同様、`toJson` メソッドは再帰的であるため、すべての属性とリレーションが JSON に変換されます。 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) の JSON エンコード オプションを指定することもできます。

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
あるいは、モデルまたはコレクションを文字列にcastすることもできます。これにより、モデルまたはコレクションに対して `toJson` メソッドが自動的に呼び出されます。

```php
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
モデルとコレクションは文字列にcastされるときに JSON に変換されるため、アプリケーションのルートまたはコントローラから直接 Eloquent オブジェクトを返すことができます。 Laravel は、Eloquent モデルとコレクションがルートまたはコントローラから返されると、自動的に JSON にシリアル化します。

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
Eloquent モデルが JSON に変換されると、ロードされたリレーションシップが JSON オブジェクトの属性として自動的に組み込まれます。また、Eloquent リレーションシップ メソッドは「キャメル ケース」メソッド名を使用して定義されますが、リレーションシップの JSON 属性は「スネーク ケース」になります。

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, you may use the `Hidden` attribute on your model. Attributes that are listed in the `Hidden` attribute will not be included in the serialized representation of your model: -->
場合によっては、モデルの配列または JSON 表現に含まれるパスワードなどの属性を制限したい場合があります。これを行うには、モデルで `Hidden` 属性を使用できます。 `Hidden` 属性にリストされている属性は、モデルのシリアル化された表現には含まれません。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}
```


> [!NOTE]
> リレーションシップを非表示にするには、リレーションシップのメソッド名を Eloquent モデルの `Hidden` 属性に追加します。

<!-- Alternatively, you may use the `Visible` attribute to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `Visible` attribute will be hidden when the model is converted to an array or JSON: -->
あるいは、`Visible` 属性を使用して、モデルの配列および JSON 表現に含める必要がある属性の「許可リスト」を定義することもできます。 `Visible` 属性に存在しないすべての属性は、モデルが配列または JSON に変換されるときに非表示になります。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
<!-- #### Temporarily Modifying Attribute Visibility -->
#### Temporarily Modifying Attribute Visibility

<!-- If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` or `mergeVisible` methods. The `makeVisible` method returns the model instance: -->
通常非表示の属性を特定のモデル インスタンスで表示したい場合は、`makeVisible` メソッドまたは `mergeVisible` メソッドを使用できます。 `makeVisible` メソッドはモデル インスタンスを返します。

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` or `mergeHidden` methods: -->
同様に、通常は表示される一部の属性を非表示にしたい場合は、`makeHidden` メソッドまたは `mergeHidden` メソッドを使用できます。

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
すべての表示属性または非表示属性を一時的にオーバーライドしたい場合は、それぞれ `setVisible` メソッドと `setHidden` メソッドを使用できます。

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values to JSON -->
## Appending Values to JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/master/eloquent-mutators) for the value: -->
場合によっては、モデルを配列または JSON に変換するときに、データベースに対応する列がない属性を追加したい場合があります。これを行うには、まず値の [accessor](/docs/master/eloquent-mutators) を定義します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

<!-- If you would like the accessor to always be appended to your model's array and JSON representations, you may use the `Appends` attribute on your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
accessorを常にモデルの配列および JSON 表現に追加したい場合は、モデルで `Appends` 属性を使用できます。accessorの PHP メソッドが「キャメル ケース」を使用して定義されている場合でも、属性名は通常、「スネーク ケース」のシリアル化表現を使用して参照されることに注意してください。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}
```

<!-- Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON representations. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model. -->
属性が `appends` リストに追加されると、モデルの配列と JSON 表現の両方に含まれます。 `appends` 配列の属性は、モデルで構成された `visible` および `hidden` 設定も尊重します。

<a name="appending-at-run-time"></a>
<!-- #### Appending at Run Time -->
#### Appending at Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` or `mergeAppends` methods. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
実行時に、`append` メソッドまたは `mergeAppends` メソッドを使用して追加の属性を追加するようにモデル インスタンスに指示できます。または、`setAppends` メソッドを使用して、特定のモデル インスタンスに追加されたプロパティの配列全体をオーバーライドすることもできます。

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<!-- Likewise, if you would like to remove all appended properties from a model, you may use the `withoutAppends` method: -->
同様に、追加されたプロパティをすべてモデルから削除したい場合は、`withoutAppends` メソッドを使用できます。

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
<!-- ## Date Serialization -->
## Date Serialization

<a name="customizing-the-default-date-format"></a>
<!-- #### Customizing the Default Date Format -->
#### Customizing the Default Date Format

<!-- You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database: -->
`serializeDate` メソッドをオーバーライドすることで、デフォルトのシリアル化形式をカスタマイズできます。この方法は、データベースに保存する際の日付の形式には影響しません。

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
<!-- #### Customizing the Date Format per Attribute -->
#### Customizing the Date Format per Attribute

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/master/eloquent-mutators#attribute-casting): -->
モデルの [cast declarations](/docs/master/eloquent-mutators#attribute-casting) で日付形式を指定することで、個々の Eloquent 日付属性のシリアル化形式をカスタマイズできます。

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```

