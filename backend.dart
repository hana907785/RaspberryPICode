import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/routine_group.dart';
import 'icon_editor.dart';
import '../bluetooth/bluetooth.dart';
import '../db/database.dart';

Future<void> showRoutineAddDialog(
    BuildContext context,
    void Function(RoutineGroup) onAdd,
    ) async {
  final TextEditingController routineNameController = TextEditingController();
  List<Map<String, dynamic>> detailItems = [];
  TimeOfDay selectedTime = const TimeOfDay(hour: 6, minute: 30);
  bool isTimerMode = false;
  String selectedIconPath = iconPaths.first;
  String selectedDetailIconPath = iconPaths.first;
  int totalMinutes = 30;
  int restMinutes = 10;
  int repeatCount = 3;

  await showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (_) => StatefulBuilder(
      builder: (ctx, setStateDialog) => ScaffoldMessenger(
        child: Scaffold(
          resizeToAvoidBottomInset: true,
          backgroundColor: Colors.transparent,
          body: Builder(
            builder: (scaffoldCtx) => Wrap(
              children: [
                Padding(
                  padding: EdgeInsets.only(
                    bottom: MediaQuery.of(ctx).viewInsets.bottom,
                    left: 24,
                    right: 24,
                    top: 24,
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      GestureDetector(
                        onTap: () => _showIconPickerDialog(
                          ctx,
                          selectedIconPath,
                          setStateDialog,
                              (newPath) => selectedIconPath = newPath,
                        ),
                        child: CircleAvatar(
                          radius: 40,
                          backgroundColor: Colors.grey[200],
                          child: ClipOval(
                            child: Image.asset(
                              selectedIconPath,
                              width: 70,
                              height: 80,
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextField(
                        controller: routineNameController,
                        textAlign: TextAlign.center,
                        decoration: const InputDecoration(
                          hintText: '루틴 이름',
                          border: InputBorder.none,
                        ),
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const Divider(),
                      Opacity(
                        opacity: isTimerMode ? 0.4 : 1.0,
                        child: IgnorePointer(
                          ignoring: isTimerMode,
                          child: Column(
                            children: [
                              DetailItemEditor(
                                selectedIconPath: selectedDetailIconPath,
                                onIconChanged: (path) => setStateDialog(() => selectedDetailIconPath = path),
                                onAdd: (item) {
                                  if (item['text'] != null && item['text'].toString().isNotEmpty) {
                                    setStateDialog(() => detailItems.add(item));
                                  }
                                },
                              ),
                              const SizedBox(height: 12),
                              ...detailItems.asMap().entries.map((entry) {
                                final index = entry.key;
                                final item = entry.value;
                                return ListTile(
                                  leading: CircleAvatar(
                                    backgroundImage: AssetImage(item['iconPath']),
                                  ),
                                  title: Text(item['text']),
                                  trailing: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Padding(
                                        padding: const EdgeInsets.only(right: 8.0),
                                        child: Text('${item['minutes']}분'),
                                      ),
                                      GestureDetector(
                                        onTap: () => setStateDialog(() => detailItems.removeAt(index)),
                                        child: const Icon(Icons.delete, size: 18, color: Colors.redAccent),
                                      ),
                                    ],
                                  ),
                                );
                              }).toList(),
                              const SizedBox(height: 20),
                            ],
                          ),
                        ),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "    시작 시간",
                            style: TextStyle(
                              fontSize: 16,
                              color: isTimerMode ? Colors.grey : Colors.black,
                            ),
                          ),
                          Switch(
                            value: isTimerMode,
                            onChanged: (val) => setStateDialog(() => isTimerMode = val),
                            activeColor: Colors.lightBlueAccent,
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      GestureDetector(
                        onTap: () async {
                          if (isTimerMode) return;
                          final picked = await showTimePicker(
                            context: context,
                            initialTime: selectedTime,
                          );
                          if (picked != null) {
                            setStateDialog(() => selectedTime = picked);
                          }
                        },
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                          decoration: BoxDecoration(
                            color: Colors.grey[200],
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                selectedTime.period == DayPeriod.am ? '오전' : '오후',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: !isTimerMode ? Colors.black : Colors.grey,
                                  fontWeight: !isTimerMode ? FontWeight.w600 : FontWeight.w400,
                                ),
                              ),
                              const SizedBox(width: 12),
                              Text(
                                selectedTime.hourOfPeriod.toString().padLeft(2, '0'),
                                style: TextStyle(
                                  fontSize: 16,
                                  color: !isTimerMode ? Colors.black : Colors.grey,
                                  fontWeight: !isTimerMode ? FontWeight.w600 : FontWeight.w400,
                                ),
                              ),
                              const SizedBox(width: 4),
                              const Text(":", style: TextStyle(fontSize: 16, color: Colors.grey)),
                              const SizedBox(width: 4),
                              Text(
                                selectedTime.minute.toString().padLeft(2, '0'),
                                style: TextStyle(
                                  fontSize: 16,
                                  color: !isTimerMode ? Colors.black : Colors.grey,
                                  fontWeight: !isTimerMode ? FontWeight.w600 : FontWeight.w400,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: [
                              Text("수행 시간", style: TextStyle(fontSize: 16, color: isTimerMode ? Colors.black : Colors.grey)),
                              Text("휴식 시간", style: TextStyle(fontSize: 16, color: isTimerMode ? Colors.black : Colors.grey)),
                              Text("반복 횟수", style: TextStyle(fontSize: 16, color: isTimerMode ? Colors.black : Colors.grey)),
                            ],
                          ),
                          const SizedBox(height: 6),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 15),
                            decoration: BoxDecoration(
                              color: Colors.grey[200],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Row(
                              children: [
                                Expanded(child: _buildDropdown("총", totalMinutes, (v) => setStateDialog(() => totalMinutes = v ?? totalMinutes), !isTimerMode)),
                                const SizedBox(width: 8),
                                const Text(":", style: TextStyle(fontSize: 16)),
                                const SizedBox(width: 8),
                                Expanded(child: _buildDropdown("휴식", restMinutes, (v) => setStateDialog(() => restMinutes = v ?? restMinutes), !isTimerMode)),
                                const SizedBox(width: 8),
                                const Text(":", style: TextStyle(fontSize: 16)),
                                const SizedBox(width: 8),
                                Expanded(child: _buildDropdown("횟수", repeatCount, (v) => setStateDialog(() => repeatCount = v ?? repeatCount), !isTimerMode)),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: () async {
                          final name = routineNameController.text.trim();
                          if (name.isEmpty) {
                            ScaffoldMessenger.of(scaffoldCtx).showSnackBar(
                              const SnackBar(content: Text("루틴 이름을 입력해주세요.")),
                            );
                            return;
                          }

                          if (selectedIconPath.contains('empty.jpg')) {
                            ScaffoldMessenger.of(scaffoldCtx).showSnackBar(
                              const SnackBar(content: Text("메인 아이콘을 선택해주세요.")),
                            );
                            return;
                          }

                          if (!isTimerMode) {
                            if (detailItems.isEmpty) {
                              ScaffoldMessenger.of(scaffoldCtx).showSnackBar(
                                const SnackBar(content: Text("세부 루틴을 하나 이상 추가해주세요.")),
                              );
                              return;
                            }

                            final hasEmptyIcon = detailItems.any((item) => item['iconPath'].contains('empty.jpg'));
                            if (hasEmptyIcon) {
                              ScaffoldMessenger.of(scaffoldCtx).showSnackBar(
                                const SnackBar(content: Text("세부 루틴의 아이콘을 모두 선택해주세요.")),
                              );
                              return;
                            }

                            final hasIncompleteItem = detailItems.any((item) =>
                            (item['text'] == null || item['text'].toString().trim().isEmpty) ||
                                (item['iconPath'] == null || item['iconPath'].contains('empty.jpg')) ||
                                (item['minutes'] == null));

                            if (hasIncompleteItem) {
                              ScaffoldMessenger.of(scaffoldCtx).showSnackBar(
                                const SnackBar(content: Text("모든 세부 루틴 항목을 완성해주세요.")),
                              );
                              return;
                            }
                          }

                          final nowDate = DateTime.now().toUtc().add(const Duration(hours: 9));
                          final formattedDate = DateFormat('yyyy-MM-dd').format(nowDate);

                          final newGroup = RoutineGroup(
                            name: name,
                            iconPath: selectedIconPath,
                            items: !isTimerMode
                                ? detailItems.map((e) => RoutineItem(
                              title: e['text'],
                              iconPath: e['iconPath'],
                              durationMinutes: e['minutes'],
                              checked: 0,
                            )).toList()
                                : [],
                            startTime: !isTimerMode ? selectedTime : null,
                            totalMinutes: isTimerMode ? totalMinutes : null,
                            restMinutes: isTimerMode ? restMinutes : null,
                            repeatCount: isTimerMode ? repeatCount : null,
                            type: isTimerMode ? 1 : 0,
                            date: formattedDate,
                          );

                          final savedGroup = await RoutineDatabase.instance.insertRoutine(newGroup);

                          String formatStartTime(TimeOfDay time) {
                            final now = DateTime.now();
                            final dt = DateTime(now.year, now.month, now.day, time.hour, time.minute);
                            return DateFormat('HH:mm:ss').format(dt);
                          }

                          String stripIconPath(String path) {
                            final fileName = path.split('/').last;
                            return fileName.endsWith('.jpg')
                                ? fileName.replaceAll('.jpg', '.JPG')
                                : fileName;
                          }

                          final todayStr = DateFormat('yyyy-MM-dd').format(nowDate);

                          if (savedGroup.type == 0) {
                            TimeOfDay addMinutes(TimeOfDay time, int minutesToAdd) {
                              final dt = DateTime(0, 1, 1, time.hour, time.minute);
                              final result = dt.add(Duration(minutes: minutesToAdd));
                              return TimeOfDay(hour: result.hour, minute: result.minute);
                            }

                            final List<Map<String, dynamic>> jsonList = [];
                            int offsetMinutes = 0;

                            for (final item in savedGroup.items) {
                              final itemStartTime = addMinutes(savedGroup.startTime!, offsetMinutes);
                              jsonList.add({
                                "id": item.id,
                                "type": "routine",
                                "date": todayStr,
                                "start_time": formatStartTime(itemStartTime),
                                "routine_minutes": item.durationMinutes,
                                "icon": stripIconPath(item.iconPath),
                                "routine_name": item.title,
                                "group_routine_name": savedGroup.name,
                              });
                              offsetMinutes += item.durationMinutes;
                            }

                            if (BluetoothService.instance.isConnected) {
                              await BluetoothService.instance.sendJsonList(jsonList);
                            }
                          } else if (savedGroup.type == 1) {
                            if (BluetoothService.instance.isConnected) {
                              await BluetoothService.instance.sendJson({
                                "id": savedGroup.id,
                                "type": "timer",
                                "timer_minutes": savedGroup.totalMinutes,
                                "rest": savedGroup.restMinutes,
                                "repeat_count": savedGroup.repeatCount,
                                "icon": stripIconPath(savedGroup.iconPath)
                              });
                            }
                          }

                          onAdd(savedGroup);
                          Navigator.pop(context);
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.black,
                          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                        child: const Text("등록하기", style: TextStyle(color: Colors.white, fontSize: 16)),
                      ),
                      const SizedBox(height: 40),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}

Widget _buildDropdown(String label, int currentValue, ValueChanged<int?> onChanged, bool disabled) {
  return SizedBox(
    width: 60,
    child: DropdownButtonFormField<int>(
      value: currentValue,
      decoration: const InputDecoration(
        isDense: true,
        contentPadding: EdgeInsets.symmetric(horizontal: 8),
        border: InputBorder.none,
      ),
      style: TextStyle(fontSize: 16, color: disabled ? Colors.grey : Colors.black),
      items: List.generate(60, (i) => i + 1).map((v) => DropdownMenuItem(
        value: v,
        child: Text(
          label == "횟수" ? "$v회" : "$v분",
          style: TextStyle(color: disabled ? Colors.grey : Colors.black),
        ),
      )).toList(),
      onChanged: disabled ? null : onChanged,
    ),
  );
}

void _showIconPickerDialog(
    BuildContext context,
    String selectedIconPath,
    StateSetter setStateDialog,
    void Function(String) onIconSelected,
    ) {
  showModalBottomSheet(
    context: context,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (_) => Padding(
      padding: const EdgeInsets.all(20),
      child: GridView.builder(
        shrinkWrap: true,
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 4,
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
        ),
        itemCount: iconPaths.length,
        itemBuilder: (context, index) {
          final path = iconPaths[index];
          return GestureDetector(
            onTap: () {
              setStateDialog(() => onIconSelected(path));
              Navigator.pop(context);
            },
            child: CircleAvatar(
              backgroundImage: AssetImage(path),
            ),
          );
        },
      ),
    ),
  );
}
