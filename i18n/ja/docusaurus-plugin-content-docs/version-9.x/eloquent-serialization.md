<!-- # Eloquent: Serialization -->
# Eloquent: Serialization

- [Introduction](#introduction)
- [Serializing Models & Collections](#serializing-models-and-collections)
    - [Serializing To Arrays](#serializing-to-arrays)
    - [Serializing To JSON](#serializing-to-json)
- [Hiding Attributes From JSON](#hiding-attributes-from-json)
- [Appending Values To JSON](#appending-values-to-json)
- [Date Serialization](#date-serialization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When building APIs using Laravel, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in the serialized representation of your models. -->
Laravel を使用して API を構築する場合、多くの場合、モデルと関係を配列または JSON に変換する必要があります。 Eloquent には、これらの変換を行うだけでなく、モデルのシリアル化された表現にどの属性を含めるかを制御するための便利なメソッドが含まれています。

> [!NOTE]
> Eloquent モデルとコレクションの JSON シリアル化を処理するさらに堅牢な方法については、[Eloquent API resources](/docs/9.x/eloquent-resources) のドキュメントを確認してください。

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models & Collections -->
## Serializing Models & Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing To Arrays -->
### Serializing To Arrays

<!-- To convert a model and its loaded [relationships](/docs/9.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
モデルとそのロードされた [relationships](/docs/9.x/eloquent-relationships) を配列に変換するには、`toArray` メソッドを使用する必要があります。このメソッドは再帰的であるため、すべての属性とすべての関係 (関係の関係を含む) が配列に変換されます。

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` メソッドは、モデルの属性を配列に変換するために使用できますが、その関係は変換できません。

```
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/9.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
コレクション インスタンスで `toArray` メソッドを呼び出して、モデルの [collections](/docs/9.x/eloquent-collections) 全体を配列に変換することもできます。

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing To JSON -->
### Serializing To JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
モデルを JSON に変換するには、`toJson` メソッドを使用する必要があります。 `toArray` と同様、`toJson` メソッドは再帰的であるため、すべての属性とリレーションが JSON に変換されます。 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) の JSON エンコード オプションを指定することもできます。

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
あるいは、モデルまたはコレクションを文字列にcastすることもできます。これにより、モデルまたはコレクションに対して `toJson` メソッドが自動的に呼び出されます。

```
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
モデルとコレクションは文字列にcastされるときに JSON に変換されるため、アプリケーションのルートまたはコントローラから直接 Eloquent オブジェクトを返すことができます。 Laravel は、Eloquent モデルとコレクションがルートまたはコントローラから返されると、自動的に JSON にシリアル化します。

```
Route::get('users', function () {
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

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. Attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model: -->
場合によっては、モデルの配列または JSON 表現に含まれるパスワードなどの属性を制限したい場合があります。これを行うには、`$hidden` プロパティをモデルに追加します。 `$hidden` プロパティの配列にリストされている属性は、モデルのシリアル化された表現には含まれません。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> リレーションシップを非表示にするには、リレーションシップのメソッド名を Eloquent モデルの `$hidden` プロパティに追加します。

<!-- Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON: -->
あるいは、`visible` プロパティを使用して、モデルの配列および JSON 表現に含める必要がある属性の「許可リスト」を定義することもできます。 `$visible` 配列に存在しないすべての属性は、モデルが配列または JSON に変換されるときに非表示になります。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be visible in arrays.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
<!-- #### Temporarily Modifying Attribute Visibility -->
#### Temporarily Modifying Attribute Visibility

<!-- If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` method. The `makeVisible` method returns the model instance: -->
特定のモデル インスタンスで通常非表示の属性を表示したい場合は、`makeVisible` メソッドを使用できます。 `makeVisible` メソッドはモデル インスタンスを返します。

```
return $user->makeVisible('attribute')->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` method. -->
同様に、通常は表示される一部の属性を非表示にしたい場合は、`makeHidden` メソッドを使用できます。

```
return $user->makeHidden('attribute')->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
すべての表示属性または非表示属性を一時的にオーバーライドしたい場合は、それぞれ `setVisible` メソッドと `setHidden` メソッドを使用できます。

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values To JSON -->
## Appending Values To JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/9.x/eloquent-mutators) for the value: -->
場合によっては、モデルを配列または JSON に変換するときに、データベースに対応する列がない属性を追加したい場合があります。これを行うには、まず値の [accessor](/docs/9.x/eloquent-mutators) を定義します。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     *
     * @return \Illuminate\Database\Eloquent\Casts\Attribute
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

<!-- After creating the accessor, add the attribute name to the `appends` property of your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
accessorを作成した後、モデルの `appends` プロパティに属性名を追加します。accessorの PHP メソッドが「キャメル ケース」を使用して定義されている場合でも、属性名は通常、「スネーク ケース」のシリアル化表現を使用して参照されることに注意してください。

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The accessors to append to the model's array form.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

<!-- Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON representations. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model. -->
属性が `appends` リストに追加されると、モデルの配列と JSON 表現の両方に含まれます。 `appends` 配列の属性は、モデルで構成された `visible` および `hidden` 設定も尊重します。

<a name="appending-at-run-time"></a>
<!-- #### Appending At Run Time -->
#### Appending At Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` method. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
実行時に、`append` メソッドを使用して追加の属性を追加するようにモデル インスタンスに指示できます。または、`setAppends` メソッドを使用して、特定のモデル インスタンスに追加されたプロパティの配列全体をオーバーライドすることもできます。

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
<!-- ## Date Serialization -->
## Date Serialization

<a name="customizing-the-default-date-format"></a>
<!-- #### Customizing The Default Date Format -->
#### Customizing The Default Date Format

<!-- You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database: -->
`serializeDate` メソッドをオーバーライドすることで、デフォルトのシリアル化形式をカスタマイズできます。この方法は、データベースに保存する際の日付の形式には影響しません。

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

<a name="customizing-the-date-format-per-attribute"></a>
<!-- #### Customizing The Date Format Per Attribute -->
#### Customizing The Date Format Per Attribute

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/9.x/eloquent-mutators#attribute-casting): -->
モデルの [cast declarations](/docs/9.x/eloquent-mutators#attribute-casting) で日付形式を指定することで、個々の Eloquent 日付属性のシリアル化形式をカスタマイズできます。

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```

