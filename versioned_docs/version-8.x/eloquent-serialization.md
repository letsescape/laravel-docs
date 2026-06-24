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
Laravel로 API를 구축할 때는 모델 및 연관관계를 배열 또는 JSON으로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 손쉽게 처리할 수 있는 메서드를 제공하며, 직렬화된 모델 표현에서 포함할 속성을 제어할 수 있는 기능도 지원합니다.

> [!TIP]
> Eloquent 모델 및 컬렉션의 JSON 직렬화를 보다 강력하게 다루고 싶다면 [Eloquent API resources](/docs/8.x/eloquent-resources) 문서도 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models & Collections -->
## Serializing Models & Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing To Arrays -->
### Serializing To Arrays

<!-- To convert a model and its loaded [relationships](/docs/8.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
모델과 로드된 [relationships](/docs/8.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모든 속성과 연관관계(심지어 연관관계의 연관관계까지)도 배열로 변환됩니다.

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` 메서드를 사용하면, 모델의 속성만 배열로 변환할 수 있으며 연관관계는 배열에 포함되지 않습니다.

```
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/8.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
또한, 모델 [collections](/docs/8.x/eloquent-collections) 전체를 컬렉션 인스턴스에서 `toArray`를 호출하여 배열로 변환할 수도 있습니다.

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing To JSON -->
### Serializing To JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
모델을 JSON으로 변환하려면 `toJson` 메서드를 사용하면 됩니다. `toArray`와 마찬가지로, `toJson`도 재귀적으로 동작하여 모든 속성과 연관관계를 JSON으로 변환합니다. 또한 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션도 지정할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
또는, 모델이나 컬렉션을 문자열로 형변환하면 자동으로 해당 객체의 `toJson` 메서드가 호출됩니다.

```
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
모델이나 컬렉션을 문자열로 변환할 때 자동으로 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트 혹은 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화하여 반환합니다.

```
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
Eloquent 모델이 JSON으로 변환될 때, 로드된 연관관계는 자동으로 JSON 객체의 속성으로 포함됩니다. 참고로, Eloquent 연관관계 메서드는 "카멜 케이스"로 정의되지만, JSON으로 직렬화된 속성명은 "스네이크 케이스"로 변환됩니다.

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. In attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model: -->
때로는 비밀번호와 같이 모델의 배열 또는 JSON 표현에서 일부 속성을 제외하고 싶을 수 있습니다. 이 경우, 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 나열된 속성들은 직렬화된 모델에서 포함되지 않습니다.

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

> [!TIP]
> 연관관계를 숨기고 싶다면, `$hidden` 속성 배열에 해당 연관관계의 메서드명을 추가하면 됩니다.

<!-- Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON: -->
반대로, `visible` 속성을 사용해 배열 및 JSON 표현에 포함될 속성의 "허용 목록"을 정의할 수도 있습니다. `$visible` 배열에 나열되지 않은 모든 속성은 배열이나 JSON 변환 시 숨겨집니다.

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
일반적으로 숨겨져 있는 특정 속성을 일시적으로 보이도록 하려면 `makeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```
return $user->makeVisible('attribute')->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` method. -->
반대로, 일반적으로 보이는 속성을 일시적으로 숨기고 싶다면 `makeHidden` 메서드를 사용할 수 있습니다.

```
return $user->makeHidden('attribute')->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values To JSON -->
## Appending Values To JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/8.x/eloquent-mutators) for the value: -->
모델을 배열 또는 JSON으로 변환할 때, 데이터베이스 컬럼에는 존재하지 않는 속성을 추가하고 싶을 때가 있습니다. 이 경우, 먼저 해당 값을 위한 [accessor](/docs/8.x/eloquent-mutators)를 정의하십시오.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     *
     * @return bool
     */
    public function getIsAdminAttribute()
    {
        return $this->attributes['admin'] === 'yes';
    }
}
```

<!-- After creating the accessor, add the attribute name to the `appends` property of your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
accessor를 만들었다면, 모델의 `appends` 속성에 해당 속성명을 추가합니다. 참고로, accessor의 PHP 메서드는 "카멜 케이스"로 정의하지만, 직렬화 시에는 "스네이크 케이스" 이름으로 지정하는 것이 일반적입니다.

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
`appends` 목록에 속성이 추가되면, 모델을 배열이나 JSON으로 변환할 때 해당 속성이 포함됩니다. `appends` 배열에 포함된 속성도 모델의 `visible` 및 `hidden` 설정을 따라 동작합니다.

<a name="appending-at-run-time"></a>
<!-- #### Appending At Run Time -->
#### Appending At Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` method. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
실행 중 특정 모델 인스턴스에 추가적인 속성을 포함하고 싶다면 `append` 메서드를 사용할 수 있습니다. 또는 `setAppends` 메서드를 사용하여 추가 속성 배열 전체를 지정할 수도 있습니다.

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
기본 직렬화 날짜 포맷을 변경하고 싶다면, `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜의 포맷에는 영향을 주지 않습니다.

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

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/8.x/eloquent-mutators#attribute-casting): -->
개별 Eloquent 날짜 속성의 직렬화 포맷을 변경하고 싶다면, 모델의 [cast declarations](/docs/8.x/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정할 수 있습니다.

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```
