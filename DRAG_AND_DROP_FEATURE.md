# Note Taking App - Drag and Drop Feature

## Overview

This note-taking application now includes a **drag and drop** feature that allows users to reorder their notes by simply dragging them to new positions in the notes list.

## Features Added

### 1. Database Schema Update
- Added `order_index` column to the `note` table to track note ordering
- Created a migration script (`migrate_add_order_index.py`) to update existing databases
- Notes are now fetched in order by `order_index` ascending, then by `updated_at` descending

### 2. Backend API Enhancement
- **New endpoint**: `PUT /api/notes/reorder`
  - Accepts a JSON payload with `note_ids` array in the desired order
  - Updates the `order_index` for each note based on its position in the array
  - Returns success/error response

### 3. Frontend Drag and Drop Implementation
- **HTML5 Drag and Drop API** integration
- **Visual feedback** during dragging:
  - Dragged item becomes semi-transparent and rotated
  - Drop targets show visual indicators
  - Notes list background changes when drag is active

### 4. User Experience Improvements
- **Intuitive interaction**: Click and drag any note to reorder
- **Real-time updates**: Order changes are immediately visible
- **Persistent ordering**: New order is saved to the database
- **Error handling**: Graceful fallback if reordering fails

## How to Use

### For Users:
1. **Open the application** in your web browser
2. **View your notes** in the left sidebar
3. **Click and hold** any note item to start dragging
4. **Drag the note** to your desired position
5. **Release** to drop the note in its new position
6. The new order is automatically saved

### Visual Cues:
- **Grab cursor** (🫴) appears when hovering over notes
- **Grabbing cursor** (✊) appears when dragging
- **Dragged note** becomes semi-transparent with a slight rotation
- **Drop zones** show a blue border indicator
- **Success message** confirms when reordering is saved

## Technical Implementation

### Database Changes
```sql
ALTER TABLE note ADD COLUMN order_index INTEGER DEFAULT 0;
```

### API Endpoint
```http
PUT /api/notes/reorder
Content-Type: application/json

{
  "note_ids": [3, 1, 4, 2]
}
```

### Frontend JavaScript
- `handleDragStart()` - Initiates drag operation
- `handleDragOver()` - Shows drop indicators
- `handleDrop()` - Processes the drop and reorders notes
- `reorderNotes()` - Updates local state and syncs with backend

### CSS Styling
```css
.note-item {
  cursor: grab;
  draggable: true;
}

.note-item.dragging {
  opacity: 0.5;
  transform: rotate(5deg);
}

.note-item.drag-over {
  border-top: 3px solid #667eea;
}
```

## Installation and Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run database migration** (for existing databases):
   ```bash
   python3 migrate_add_order_index.py
   ```

3. **Start the application**:
   ```bash
   python3 src/main.py
   ```

4. **Open in browser**: http://localhost:5000

## Testing

### Manual Testing
1. Create multiple notes
2. Try dragging notes to different positions
3. Refresh the page to verify persistence
4. Test with search results

### API Testing
Use the provided `test_api.http` file or `test_drag_drop.py` script:
```bash
python3 test_drag_drop.py
```

## Browser Compatibility

The drag and drop feature uses HTML5 APIs and works in:
- ✅ Chrome 4+
- ✅ Firefox 3.5+
- ✅ Safari 3.1+
- ✅ Edge (all versions)
- ✅ Mobile browsers with touch support

## Accessibility

- **Keyboard navigation**: Notes remain accessible via Tab key
- **Screen readers**: Proper ARIA labels maintained
- **Visual indicators**: Clear feedback for drag states
- **Touch support**: Works on mobile devices

## Error Handling

- **Network errors**: Automatic retry with user feedback
- **Invalid operations**: Prevents dropping on same position
- **Database errors**: Graceful rollback with error messages
- **State recovery**: Reloads notes if reordering fails

## Future Enhancements

Potential improvements for the drag and drop feature:
- Multi-select dragging
- Nested folder organization
- Drag to delete functionality
- Undo/redo operations
- Keyboard shortcuts for reordering
- Animation improvements

## Troubleshooting

### Common Issues

1. **"order_index column doesn't exist"**
   - Run the migration: `python3 migrate_add_order_index.py`

2. **Drag and drop not working**
   - Check browser console for JavaScript errors
   - Ensure the Flask app is running
   - Verify API endpoints are accessible

3. **Order not persisting**
   - Check network tab for failed API calls
   - Verify database write permissions
   - Check Flask app logs for errors

### Debugging

Enable debug mode in Flask for detailed error messages:
```python
app.run(debug=True)
```

Check the browser's developer tools console for any JavaScript errors during drag operations.

## Contributing

To contribute to the drag and drop feature:
1. Test the functionality thoroughly
2. Add unit tests for new API endpoints
3. Ensure backward compatibility
4. Update documentation for any changes
5. Follow the existing code style and patterns

---

*This drag and drop implementation provides a smooth, intuitive way for users to organize their notes exactly as they prefer.*