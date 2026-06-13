# Personal Blog - 使用说明

## 功能特性
- 文章标题、内容（支持 Markdown）
- 文章分类和标签
- 现代化 Bootstrap 5 界面
- 完整的 CRUD 操作

## 安装步骤

1. 安装依赖：
```bash
pip install django markdown
```

2. 应用数据库迁移：
```bash
python manage.py migrate
```

3. 创建超级用户（可选，用于 Admin 后台）：
```bash
python manage.py createsuperuser
```

4. 启动开发服务器：
```bash
python manage.py runserver
```

## 访问地址

- 博客首页：http://127.0.0.1:8000/personal_blog/
- 创建文章：http://127.0.0.1:8000/personal_blog/post/new/
- Admin 后台：http://127.0.0.1:8000/admin/

## Markdown 示例

你可以在文章内容中使用 Markdown 格式：

```markdown
# 标题
这是一段普通文字。

## 二级标题
- 列表项 1
- 列表项 2

**粗体文字** 和 *斜体文字*

```python
# 代码块
print("Hello, World!")
```
```
