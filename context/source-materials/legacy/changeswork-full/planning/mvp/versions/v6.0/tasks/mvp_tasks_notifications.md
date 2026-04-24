# Задачи для системы уведомлений (Notifications)

## Обзор

**Компонент:** Система уведомлений
**Статус:** Новая разработка

### Что реализуется:

**Email уведомления для событий:**
- Отправка на согласование (Pilot/Change/Package)
- Согласование этапа (переход к следующему этапу)
- Утверждение (завершение процесса)
- Отклонение (возврат на доработку)
- Отзыв с согласования
- Активация Pilot
- Внедрение Deployment
- Rollback Deployment

**Шаблоны уведомлений:**
- Шаблон для отправки на согласование (с таблицей элементов)
- Шаблон для согласования/утверждения
- Шаблон для отклонения (с причиной)
- Шаблон для отзыва
- Шаблон для активации/внедрения
- Шаблон для rollback

**Получатели:**
- Согласующие (при отправке на согласование)
- Автор (при согласовании/отклонении/завершении)
- Утверждающий (при переходе к этапу утверждения)

---

## BE-NOT1: Backend для системы уведомлений

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 5 дней

### Summary
Реализация системы email уведомлений для всех событий процесса согласования

### Description

Реализовать систему уведомлений:

1. **Модель данных Notification:**

   ```python
   class Notification(models.Model):
       """Уведомление"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)

       # Получатель
       recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

       # Тип уведомления
       notification_type = models.CharField(
           max_length=50,
           choices=[
               ('approval_request', 'Запрос на согласование'),
               ('approval_approved', 'Согласовано'),
               ('approval_rejected', 'Отклонено'),
               ('approval_completed', 'Утверждено'),
               ('approval_recalled', 'Отозвано'),
               ('pilot_activated', 'Пилот активирован'),
               ('change_deployed', 'Внедрение внедрено'),
               ('change_rolled_back', 'Внедрение откачено')
           ]
       )

       # Связь с сущностью
       entity_type = models.CharField(max_length=50)  # 'pilot', 'change', 'package'
       entity_id = models.UUIDField()

       # Содержимое
       subject = models.CharField(max_length=255)
       body = models.TextField()

       # Метаданные
       sent_at = models.DateTimeField(auto_now_add=True)
       read_at = models.DateTimeField(null=True, blank=True)

       class Meta:
           db_table = 'notification'
           indexes = [
               models.Index(fields=['recipient', 'read_at']),
               models.Index(fields=['entity_type', 'entity_id']),
           ]
   ```

2. **Email шаблоны:**

   **Базовый шаблон (base_email.html):**
   - Шапка: логотип Сбербанк, зеленый фон
   - Тело: динамический контент
   - Футер: "Это автоматическое уведомление. Пожалуйста, не отвечайте на это письмо."

   **Шаблон для отправки на согласование (approval_request.html):**
   - Приветствие
   - Текст: "Направляем на согласование изменения риск-стратегий:"
   - Таблица элементов (ID, Название, Статус)
   - Кнопка "Перейти к согласованию" (ссылка на систему)
   - Подпись: "Система управления изменениями риск-стратегий"

   **Шаблон для согласования (approval_approved.html):**
   - Приветствие
   - Текст: "Ваше изменение {название} успешно согласовано"
   - Информация об элементе (ID, Название, Статус)
   - Кнопка "Перейти к элементу"

   **Шаблон для отклонения (approval_rejected.html):**
   - Приветствие
   - Текст: "Ваше изменение {название} отклонено"
   - Причина отклонения (красный блок)
   - Информация об элементе
   - Кнопка "Перейти к элементу"

3. **Сервис отправки уведомлений:**

   ```python
   class NotificationService:
       """Сервис отправки уведомлений"""

       @staticmethod
       def send_approval_request(workflow, recipients):
           """Отправка запроса на согласование"""
           items = get_workflow_items(workflow)

           for recipient in recipients:
               subject = f"Направлено на согласование: {len(items)} элемент(ов)"
               body = render_template('approval_request.html', {
                   'recipient': recipient,
                   'items': items,
                   'workflow': workflow
               })

               # Отправка email
               send_email(
                   to=recipient.email,
                   subject=subject,
                   body=body
               )

               # Сохранение в БД
               Notification.objects.create(
                   recipient=recipient,
                   notification_type='approval_request',
                   entity_type=workflow.entity_type,
                   entity_id=workflow.entity_id,
                   subject=subject,
                   body=body
               )

       @staticmethod
       def send_approval_approved(workflow, author):
           """Отправка уведомления об согласовании"""
           items = get_workflow_items(workflow)

           subject = f"Согласовано: {len(items)} элемент(ов)"
           body = render_template('approval_approved.html', {
               'recipient': author,
               'items': items,
               'workflow': workflow
           })

           send_email(to=author.email, subject=subject, body=body)

           Notification.objects.create(
               recipient=author,
               notification_type='approval_approved',
               entity_type=workflow.entity_type,
               entity_id=workflow.entity_id,
               subject=subject,
               body=body
           )

       @staticmethod
       def send_approval_rejected(workflow, author, reason):
           """Отправка уведомления об отклонении"""
           items = get_workflow_items(workflow)

           subject = f"Отклонено: {len(items)} элемент(ов)"
           body = render_template('approval_rejected.html', {
               'recipient': author,
               'items': items,
               'workflow': workflow,
               'reason': reason
           })

           send_email(to=author.email, subject=subject, body=body)

           Notification.objects.create(
               recipient=author,
               notification_type='approval_rejected',
               entity_type=workflow.entity_type,
               entity_id=workflow.entity_id,
               subject=subject,
               body=body
           )
   ```

4. **Интеграция с событиями:**

   **Signals для автоматической отправки:**
   ```python
   from django.db.models.signals import post_save
   from django.dispatch import receiver

   @receiver(post_save, sender=ApprovalWorkflow)
   def handle_approval_workflow_events(sender, instance, created, **kwargs):
       """Обработка событий процесса согласования"""
       if created:
           # Отправка на согласование
           stage = instance.stages.first()
           approvers = [d.approver for d in stage.decisions.all()]
           NotificationService.send_approval_request(instance, approvers)

       elif instance.status == 'completed':
           # Согласование завершено
           NotificationService.send_approval_approved(
               instance,
               instance.submitted_by
           )

       elif instance.status == 'rejected':
           # Отклонено
           reason = get_rejection_reason(instance)
           NotificationService.send_approval_rejected(
               instance,
               instance.submitted_by,
               reason
           )

   @receiver(post_save, sender=ApprovalStage)
   def handle_stage_completion(sender, instance, **kwargs):
       """Обработка завершения этапа"""
       if instance.status == 'approved':
           # Этап согласован, переход к следующему
           next_stage = instance.workflow.stages.filter(
               order=instance.order + 1
           ).first()

           if next_stage:
               # Уведомление согласующим следующего этапа
               approvers = [d.approver for d in next_stage.decisions.all()]
               NotificationService.send_approval_request(
                   instance.workflow,
                   approvers
               )
   ```

5. **API Endpoints:**

   **GET /api/notifications/**
   - Получение списка уведомлений текущего пользователя
   - Фильтрация по read/unread
   - Пагинация

   **POST /api/notifications/{id}/mark_as_read/**
   - Отметка уведомления как прочитанного

6. **Конфигурация email:**

   ```python
   # settings.py
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.example.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'noreply@example.com'
   EMAIL_HOST_PASSWORD = 'password'
   DEFAULT_FROM_EMAIL = 'Система управления изменениями <noreply@example.com>'
   ```

### Acceptance Criteria

- [ ] Модель Notification создана
- [ ] Миграции применены
- [ ] Email шаблоны созданы (base, approval_request, approval_approved, approval_rejected)
- [ ] NotificationService реализован
- [ ] Метод send_approval_request работает
- [ ] Метод send_approval_approved работает
- [ ] Метод send_approval_rejected работает
- [ ] Signals для автоматической отправки реализованы
- [ ] Уведомления отправляются при отправке на согласование
- [ ] Уведомления отправляются при согласовании
- [ ] Уведомления отправляются при отклонении
- [ ] Уведомления отправляются при переходе к следующему этапу
- [ ] GET /api/notifications/ endpoint реализован
- [ ] POST /api/notifications/{id}/mark_as_read/ endpoint реализован
- [ ] Email конфигурация настроена
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для отправки email
- [ ] API документация обновлена

### Dependencies
- BE-AP1 (требуется процесс согласования)
- BE-INT1 (требуется интеграция ЖЦ)

---

## Итоговая зависимость задач

```
BE-AP1 (8 дней)
  ↓
BE-INT1 (3 дня)
  ↓
BE-NOT1 (5 дней)
```

**Общая длительность (критический путь):** 16 дней

---

## ✅ Ключевые особенности

1. **Email уведомления** - автоматическая отправка при событиях
2. **Шаблоны уведомлений** - HTML шаблоны с брендингом Сбербанк
3. **Модель Notification** - сохранение истории уведомлений в БД
4. **Signals для автоматической отправки** - интеграция с событиями
5. **API для уведомлений** - получение списка и отметка как прочитанного
6. **Множественные получатели** - отправка всем согласующим этапа
7. **Причина отклонения** - включение в уведомление
8. **Ссылки на систему** - кнопки "Перейти к согласованию"

---
