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
Laravel로 API를 만들다 보면, 모델과 그 연관관계 데이터를 배열이나 JSON 형태로 변환해야 하는 경우가 많습니다. Eloquent는 이런 변환을 쉽게 처리할 수 있는 편리한 메서드들과, 직렬화 결과에 포함될 속성을 제어하는 기능을 제공합니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더욱 강력하게 제어하고 싶다면 [Eloquent API resources](/docs/10.x/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models and Collections -->
## Serializing Models and Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing to Arrays -->
### Serializing to Arrays

<!-- To convert a model and its loaded [relationships](/docs/10.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
모델과 로드된 [relationships](/docs/10.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 모든 연관관계(그리고 연관관계의 연관관계까지 포함)가 배열로 변환됩니다.

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` 메서드는 모델의 속성만 배열로 변환하고, 연관관계는 포함하지 않습니다.

```
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/10.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
또한 [collections](/docs/10.x/eloquent-collections) 전체를 배열로 변환하려면 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다.

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing to JSON -->
### Serializing to JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하면 됩니다. `toArray`와 마찬가지로, `toJson`도 모든 속성과 연관관계를 재귀적으로 JSON 문자열로 변환합니다. 또한, [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션도 지정할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
또는 모델이나 컬렉션을 문자열로 casting할 수도 있는데, 이 경우 `toJson` 메서드가 자동으로 호출되어 JSON 문자열을 반환합니다.

```
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
모델과 컬렉션은 문자열로 변환될 때 JSON으로 자동 직렬화되기 때문에, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 Eloquent 모델이나 컬렉션이 반환되면 이를 자동으로 JSON으로 직렬화합니다.

```
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
Eloquent 모델이 JSON으로 변환될 때, 로드된 연관관계도 JSON 객체의 속성으로 포함됩니다. 참고로, Eloquent 연관관계 메서드는 "카멜케이스"로 정의하지만, JSON에서는 속성명이 "스네이크케이스"로 변환되어 나타납니다.

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. Attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model: -->
때로는 비밀번호 등 특정 속성을 모델의 배열이나 JSON 표현에서 제외하고 싶을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 속성의 배열에 나열된 속성들은 모델의 직렬화 결과에 포함되지 않습니다.

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
> 연관관계를 숨기고 싶을 때는, 해당 연관관계의 메서드명을 Eloquent 모델의 `$hidden` 속성에 추가하면 됩니다.

<!-- Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON: -->
반대로, `visible` 속성을 사용해서 모델의 배열 및 JSON 표현에 포함될 "허용 목록"을 정의할 수도 있습니다. `$visible` 배열에 없는 모든 속성들은 배열이나 JSON으로 변환 시 숨겨집니다.

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
평소에는 숨겨져 있는 속성을 특정 모델 인스턴스에서만 잠깐 보이게 하고 싶다면, `makeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```
return $user->makeVisible('attribute')->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` method. -->
반대로, 평소에는 보이던 속성을 일시적으로 숨기고 싶을 때는 `makeHidden` 메서드를 사용할 수 있습니다.

```
return $user->makeHidden('attribute')->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
`setVisible` 또는 `setHidden` 메서드를 사용해서 모델 인스턴스의 보이거나 숨길 속성 전체를 임시로 지정해 줄 수도 있습니다.

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values to JSON -->
## Appending Values to JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/10.x/eloquent-mutators) for the value: -->
때로는 데이터베이스 컬럼으로 존재하지 않는 속성도, 모델을 배열이나 JSON으로 변환하면서 추가하고 싶을 수 있습니다. 이럴 때는 먼저 해당 값을 위한 [accessor](/docs/10.x/eloquent-mutators)를 정의해 줍니다.

```
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

<!-- If you would like the accessor to always be appended to your model's array and JSON representations, you may add the attribute name to the `appends` property of your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
작성한 accessor가 항상 모델의 배열 및 JSON 표현에 포함되도록 하려면, 모델의 `appends` 속성에 해당 속성명을 추가하면 됩니다. accessor의 PHP 메서드는 "카멜케이스"로 정의하더라도, 속성명은 보통 "스네이크케이스" 직렬화 표현으로 참조한다는 점에 유의하시기 바랍니다.

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
`appends` 리스트에 속성이 추가되면, 해당 속성은 모델의 배열 및 JSON 표현 모두에 포함됩니다. 또한 `appends` 배열에 포함된 속성들도 모델에 설정된 `visible` 및 `hidden` 설정을 그대로 따릅니다.

<a name="appending-at-run-time"></a>
<!-- #### Appending at Run Time -->
#### Appending at Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` method. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
런타임에서, 모델 인스턴스에 추가 속성을 동적으로 추가하고 싶다면 `append` 메서드를 사용할 수 있습니다. 또는, `setAppends` 메서드로 해당 인스턴스의 appends 전체를 재설정할 수도 있습니다.

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
<!-- ## Date Serialization -->
## Date Serialization

<a name="customizing-the-default-date-format"></a>
<!-- #### Customizing the Default Date Format -->
#### Customizing the Default Date Format

<!-- You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database: -->
기본 날짜 직렬화 포맷을 바꾸고 싶다면, `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장된 날짜 포맷에는 영향을 주지 않습니다.

```
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

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/10.x/eloquent-mutators#attribute-casting): -->
모델의 [cast declarations](/docs/10.x/eloquent-mutators#attribute-casting)에서 각 Eloquent 날짜 속성의 직렬화 포맷을 별도로 지정할 수도 있습니다.

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```
