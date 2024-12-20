import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { formatDistanceToNow } from 'date-fns';
import { LuTrash2, LuSend, LuCheck, LuX, LuReply, LuChevronUp, LuChevronDown} from "react-icons/lu";
import { FiEdit2, FiMessageSquare } from "react-icons/fi";
import api from '../../../api';
import { USER_ID } from '../../../constants';
import { HiOutlineDotsVertical } from "react-icons/hi";
import { ACCESS_TOKEN } from '../../../constants';
import { useNavigate } from 'react-router-dom';

export function CommentSection({ event }) {
  const [comments, setComments] = useState([]);
  const [expandedComments, setExpandedComments] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editContent, setEditContent] = useState(''); 
  const [replyingTo, setReplyingTo] = useState(null);
  const [replyContent, setReplyContent] = useState(''); 
  const [comment, setComment] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const userId = localStorage.getItem(USER_ID);
  const navigate = useNavigate();
  const {
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm();

  const toggleReplies = (commentId) => {
    setExpandedComments(prev => 
      prev.includes(commentId)
        ? prev.filter(id => id !== commentId)
        : [...prev, commentId]
    );
  };
  
  // API endpoints
  const end_point = {
    getEventComments: async (eventId) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.get(`/events/${eventId}/comments`, { headers });
        return response.data;
      } catch (error) {
        throw new Error('Error fetching comments: ' + (error.response?.data?.detail));
      }
    },
    writeComment: async (content, eventId, parentId = null) => {
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (!token) {
        const error = new Error('Authentication required');
        error.name = 'AuthenticationError';
        throw error;
      }
    
      try {
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        
        const response = await api.post(
          `/comments/write-comment/${eventId}`,
          { content, parent_id: parentId },
          { headers }
        );
        return response.data;
      } catch (error) {
        throw error;
      }
    },
    

    deleteComment: async (commentId) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.delete(`/comments/${commentId}/delete/`, { headers });
        return response.status === 204;
      } catch (error) {
        alert('Error deleting comment: ' + (error.response?.data?.detail));
      }
    },
    editComment: async (commentId, content) => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        const response = await api.put(`/comments/${commentId}/edit/`, { content }, { headers });
        return response.data;
      } catch (error) {
        alert('Error editing comment: ' + (error.response?.data?.detail));
      }
    }
  };

  // Fetch comments on component mount or when event changes
  useEffect(() => {
    const fetchComments = async () => {
      if (!event?.id) return;
      try {
        setIsLoading(true);
        const fetchedComments = await end_point.getEventComments(event.id);
        setComments(fetchedComments);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchComments();
  }, [event?.id]);

  // Handle form submission for new comment
  const onSubmit = async () => {
    if (!event?.id || !comment.trim()) return;
    
    try {
      setIsLoading(true);
      
      // Check for authentication before attempting to post
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (!token) {
        console.error('No authentication token found');
        navigate('/login');
        
        return;
      }
  
      const newComment = await end_point.writeComment(
        replyingTo ? replyContent : comment,
        event.id,
        replyingTo ? replyingTo : null
      );
  

      setComments(prev => [newComment, ...prev]);
      setComment('');
      setReplyContent('');
      setReplyingTo(null);
      setError(null);
    } catch (error) {
      console.error('Comment submission error:', {
        message: error.message,
        response: error.response,
        fullError: error
      });

      if (error.response) {
 
        const errorMessage = error.response.data?.detail 
          || error.response.data?.message 
          || 'An error occurred while posting the comment';
        
        alert(errorMessage);
      } else if (error.request) {
        // The request was made but no response was received
        alert('No response received from server. Please check your connection.');
      } else {
        // Something happened in setting up the request
        alert('Error: ' + error.message);
      }
    } finally {
      setIsLoading(false);
    }
  };


  // Handle delete
  const handleDelete = async (commentId) => {
    try {
      setIsLoading(true);
      if (isLoading) return;
  
      // Check if the comment is a reply or a main comment
      const isReply = comments.some(comment => 
        comment.replies.some(reply => reply.id === commentId)
      );
  
      if (isReply) {
        // If it's a reply, update the specific comment replies
        setComments(prev => 
          prev.map(comment => ({
            ...comment,
            replies: comment.replies.filter(reply => reply.id !== commentId)
          }))
        );
      } else {
        // If it's a main comment, remove it from the main comments
        setComments(prev => prev.filter(comment => comment.id !== commentId));
      }
  
      await end_point.deleteComment(commentId);
    } catch (error) {
      console.error('Error deleting comment:', error);
      setError(error.message || 'An unknown error occurred');
      if (isReply) {
        const fetchedComments = await end_point.getEventComments(event.id);
        setComments(fetchedComments);
      } else {
        const fetchedComments = await end_point.getEventComments(event.id);
        setComments(fetchedComments);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle edit
  const startEditing = (comment) => {
    setEditingId(comment.id);
    setEditContent(comment.content);
    cancelReplying();
  };

  const saveEdit = async (commentId) => {
    try {
      setIsLoading(true);
      const updatedComment = await end_point.editComment(commentId, editContent);
      setComments(prev =>
        prev.map(comment => (comment.id === commentId ? updatedComment : comment))
      );
      setEditingId(null);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditContent('');
  };
  
  const startReplying = (comment) => {
    setReplyingTo(comment.id);
    cancelEditing
  };
  const saveReply = async () => {
    try {
      setIsLoading(true);
      const newReply = await end_point.writeComment(replyContent, event.id, replyingTo);

      setComments((prev) =>
        prev.map((comment) =>
          comment.id === replyingTo
            ? { ...comment, replies: [newReply, ...comment.replies] }
            : comment
        )
      );
      toggleReplies(replyingTo);
      setReplyContent('');
      setReplyingTo(null); // Reset replyingTo
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };
  const cancelReplying = () => {
    setReplyingTo(null);
    setReplyContent('');
  };
 
  const CommentContent = ({ comment, editingId, editContent, startEditing, saveEdit, cancelEditing }) => {
    return (
      <div className="flex items-start gap-3">
         <div className="avatar h-10 w-10">
          <img
            src={comment.user.profile_picture}
            alt={comment.user.name}
            className="rounded-full h-10 w-10"
          />
        </div>
        <div className="flex-1">
        <div className="flex justify-between mb-1 h-6">
          <span className="font-medium text-gray-800">{comment.user.username}</span>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">
              {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
            </span>
            {comment.user.id == userId ? (
              <div className="dropdown dropdown-end">
                <label tabIndex={0} className="btn btn-ghost btn-circle">
                  <HiOutlineDotsVertical className="w-4 h-4 text-gray-500" />
                </label>
                <ul
                  tabIndex={0}
                  className="dropdown-content menu p-2 shadow bg-white rounded-box w-32"
                >
                  <li>
                    <button onClick={() => startEditing(comment)} className="flex items-center gap-2 text-gray-600">
                      <FiEdit2 className="w-4 h-4" /> Edit
                    </button>
                  </li>
                  <li>
                    <button onClick={() => handleDelete(comment.id)} className="flex items-center gap-2 text-red-600" disabled={isLoading}>
                      <LuTrash2 className="w-4 h-4" /> {isLoading ? "Deleting..." : "Delete"}
                    </button>
                  </li>
                </ul>
              </div>
            ) : (
              <div className='w-12'></div>
            )}
          </div>
        </div>
  
        {editingId === comment.id ? (
          <div className="flex gap-2 mt-2">
            <input
              type="text"
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              className="flex-1 bg-white rounded-lg border border-gray-300 px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              autoFocus
            />
            <button
              onClick={() => saveEdit(comment.id)}
              disabled={!editContent.trim()}
              className={`p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors ${
                !editContent.trim() ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              title="Save"
            >
              <LuCheck className="w-4 h-4" />
            </button>
            <button
              onClick={cancelEditing}
              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Cancel"
            >
              <LuX className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <p className="text-gray-600 mt-2">{comment.content}</p>
        )}
        </div>
      </div>
    );
  };
  // JSX rendering the component
  return (
    <div className="bg-white rounded-xl shadow-sm flex flex-col h-[500px]" data-testid="event-comment">
      <div className="p-6 border-b">
        <div className="flex items-center gap-2">
          <FiMessageSquare className="w-5 h-5 text-dark-purple" />
          <h2 className="text-2xl font-semibold text-dark-purple">Comments</h2>
        </div>
      </div>
      {error && <div className="text-red-500 mb-4">{error}</div>}

      <div className="flex-1 overflow-y-auto p-6">
        <div className="space-y-6">
          {comments.map((comment) => (
            <div key={comment.id} className="border-b pb-4 last:border-0 flex items-start space-x-4">
              <div className="flex-1">
                <CommentContent
                  comment={comment}
                  editingId={editingId}
                  editContent={editContent}
                  startEditing={startEditing}
                  saveEdit={saveEdit}
                  cancelEditing={cancelEditing}
                />
                <div className="mt-2 mb-2 flex items-center gap-4">
                  <button
                    onClick={() => startReplying(comment)}
                    className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1"
                  >
                    <LuReply className="w-4 h-4" />
                    Reply
                  </button>
                  {comment.replies.length > 0 && (
                    <button
                      onClick={() => toggleReplies(comment.id)}
                      className="text-sm w-3/12 text-gray-500 hover:text-gray-600 flex items-center gap-1"
                    >
                      {expandedComments.includes(comment.id) ? (
                        <LuChevronUp className="w-4 h-4" />
                      ) : (
                        <LuChevronDown className="w-4 h-4" />
                      )}
                      {comment.replies.length} {comment.replies.length === 1 ? 'reply' : 'replies'}
                    </button>
                  )}
                  {replyingTo === comment.id && (
                    <div className="mt-3 mb-3 flex gap-2 items-center w-full">
                      <input
                        type="text"
                        value={replyContent}
                        onChange={(e) => setReplyContent(e.target.value)}
                        placeholder="Write a reply..."
                        className="flex-1 rounded-lg border bg-white border-gray-300 px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        autoFocus
                      />
                      <button
                        onClick={saveReply}
                        className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-1"
                      >
                        <LuSend className="w-3 h-3" />
                        Reply
                      </button>
                      <button
                        onClick={cancelReplying}
                        className="text-red-600 hover:underline"
                      >
                        <LuX className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>
                {expandedComments.includes(comment.id) && (
                  <div className="mt-4 pl-6 border-l-2 border-gray-100 space-y-4">
                    {comment.replies.map((reply) => (
                      <CommentContent
                        key={reply.id}
                        comment={reply}
                        editingId={editingId}
                        editContent={editContent}
                        startEditing={startEditing}
                        saveEdit={saveEdit}
                        cancelEditing={cancelEditing}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="p-6 border-t">
        <form onSubmit={handleSubmit(onSubmit)} className="flex gap-2">
          <input
            type="text"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Add a comment..."
            className="flex-1 bg-white rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="bg-dark-purple text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <LuSend className="w-4 h-4" />
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
