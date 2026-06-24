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
Laravel을 사용해 API를 개발할 때, 모델과 연관관계를 배열 또는 JSON 형태로 변환해야 하는 경우가 많습니다. Eloquent는 이러한 변환을 쉽게 할 수 있는 편리한 메서드들을 제공하며, 모델의 직렬화 결과에 포함될 속성을 세밀하게 제어할 수 있는 기능도 지원합니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더 강력하게 다루고 싶다면 [Eloquent API resources](/docs/9.x/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models & Collections -->
## Serializing Models & Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing To Arrays -->
### Serializing To Arrays

<!-- To convert a model and its loaded [relationships](/docs/9.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
모델과 함께 로드된 [relationships](/docs/9.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용합니다. 이 메서드는 재귀적으로 동작하기 때문에, 모든 속성과 연관관계(연관관계의 또 다른 연관관계까지 포함)까지 전부 배열로 변환됩니다.

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` 메서드는 모델의 속성만 배열로 변환하며, 연관관계는 포함하지 않습니다.

```
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/9.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
또한, 모델의 전체 [collections](/docs/9.x/eloquent-collections)을 컬렉션 인스턴스에서 `toArray` 메서드를 호출하여 배열로 변환할 수도 있습니다.

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing To JSON -->
### Serializing To JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`와 마찬가지로, `toJson` 역시 재귀적으로 모든 속성과 연관관계를 JSON으로 변환합니다. 또한 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) 어떠한 JSON 인코딩 옵션도 함께 지정할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
또는, 모델이나 컬렉션을 문자열로 casting(cast)하면 `toJson` 메서드가 자동으로 호출되어 JSON 문자열이 반환됩니다.

```
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
이처럼 모델이나 컬렉션이 문자열로 casting될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델 및 컬렉션을 자동으로 JSON으로 직렬화합니다.

```
Route::get('users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
Eloquent 모델이 JSON으로 변환될 때, 로드된 연관관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한 Eloquent 연관관계 메서드는 카멜케이스로 정의하지만, JSON의 속성명은 스네이크케이스로 변환되어 사용됩니다.

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. Attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model: -->
비밀번호처럼 모델의 배열 또는 JSON 표현에 포함하고 싶지 않은 속성이 있을 수 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 속성에 명시된 배열의 내용은 모델이 직렬화될 때 포함되지 않습니다.

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
> 연관관계를 숨기고 싶다면, 해당 연관관계의 메서드 이름을 Eloquent 모델의 `$hidden` 속성에 추가하면 됩니다.

<!-- Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON: -->
또는, `visible` 속성을 사용하여 배열 및 JSON 표현에 포함될 속성만을 "허용 목록"으로 명시할 수도 있습니다. `$visible` 배열에 포함되지 않은 모든 속성은 배열이나 JSON 변환 시 숨겨집니다.

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
일반적으로 숨겨진 속성을 일시적으로 보이게 하고 싶다면 `makeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```
return $user->makeVisible('attribute')->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` method. -->
반대로, 평소에 보이는 속성을 일시적으로 숨기고 싶다면 `makeHidden` 메서드를 사용할 수 있습니다.

```
return $user->makeHidden('attribute')->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
모델의 visible 또는 hidden 속성 전체를 일시적으로 덮어쓰려면 각각 `setVisible`과 `setHidden` 메서드를 사용하세요.

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values To JSON -->
## Appending Values To JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/9.x/eloquent-mutators) for the value: -->
모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼에 해당하지 않는 속성을 추가하고 싶을 때가 있습니다. 이럴 때는 먼저 해당 값에 대한 [accessor](/docs/9.x/eloquent-mutators)를 정의합니다.

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
그리고 나서, 생성한 속성명을 모델의 `appends` 속성에 추가합니다. 일반적으로 속성명은 직렬화된 "스네이크케이스"로 명시해야 하며, accessor의 PHP 메서드는 카멜케이스로 정의하더라도 상관없습니다.

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
이렇게 `appends` 목록에 속성을 추가하면, 그 속성이 모델의 배열 및 JSON 표현에 함께 포함됩니다. `appends` 배열의 속성도 모델에 설정된 `visible` 또는 `hidden` 옵션을 함께 따릅니다.

<a name="appending-at-run-time"></a>
<!-- #### Appending At Run Time -->
#### Appending At Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` method. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
실행 중에 모델 인스턴스에서 추가로 속성을 붙이고 싶을 때는 `append` 메서드를 사용할 수 있습니다. 또는, `setAppends` 메서드를 통해 해당 모델 인스턴스의 추가 속성 목록 전체를 덮어쓸 수도 있습니다.

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
기본 날짜 직렬화 포맷을 변경하고 싶다면 `serializeDate` 메서드를 오버라이드하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜 포맷에는 영향을 주지 않습니다.

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
특정 Eloquent 날짜 속성만 직렬화 포맷을 다르게 지정하고 싶다면, 모델의 [cast declarations](/docs/9.x/eloquent-mutators#attribute-casting)에서 날짜 포맷을 지정할 수 있습니다.

```
protected $casts = [
    'birthday' => 'date:Y-m-d',
    'joined_at' => 'datetime:Y-m-d H:00',
];
```
