from datetime import datetime
from django.db import models
from django.db.models import Q


class Tag(models.Model):
    """ タグ """
    name = models.CharField("名称", max_length=64, unique=True)

    @classmethod
    def get_or_create(cls, name):
        """ 指定された名称のタグを生成して返す、既にあればそれを取得して返す """
        ret = cls.objects.filter(name=name).first()
        if not ret:
            ret = cls.objects.create(name=name)
        return ret

    @classmethod
    def multi_get_or_create(cls, names):
        if not names:
            return []
        tags = []
        for name in names:
            tags.append(cls.get_or_create(name))
        return tags

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tag"


class Entry(models.Model):
    """ 記事 """
    day = models.DateField("日")
    title = models.CharField("タイトル", max_length=64)
    content = models.TextField("内容")
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField("登録日時", default=datetime.now)

    @classmethod
    def search(cls, keyword):
        if not keyword:
            return []
        return cls.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))

    def to_dict(self, include_fields=["id", "day", "title", "content"]):
        ret = {}
        if "id" in include_fields:
            ret["id"] = self.id,
        if "day" in include_fields:
            ret["day"] = f"{self.day:%Y-%m-%d}"
        if "title" in include_fields:
            ret["title"] = self.title
        if "content" in include_fields:
            ret["content"] = self.content
        if "tags" in include_fields:
            ret["tags"] = [tag.name for tag in self.tags.all()]
        return ret

    def __str__(self):
        return f"{self.id}:{self.title}"

    class Meta:
        db_table = "entry"
        ordering = ("-day",)