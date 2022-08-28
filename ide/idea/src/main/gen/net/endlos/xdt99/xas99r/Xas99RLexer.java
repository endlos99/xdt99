/* The following code was generated by JFlex 1.7.0 tweaked for IntelliJ platform */

package net.endlos.xdt99.xas99r;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99r.psi.Xas99RTypes;
import com.intellij.psi.TokenType;


/**
 * This class is a scanner generated by 
 * <a href="http://www.jflex.de/">JFlex</a> 1.7.0
 * from the specification file <tt>Xas99R.flex</tt>
 */
class Xas99RLexer implements FlexLexer {

  /** This character denotes the end of file */
  public static final int YYEOF = -1;

  /** initial size of the lookahead buffer */
  private static final int ZZ_BUFFERSIZE = 16384;

  /** lexical states */
  public static final int YYINITIAL = 0;
  public static final int MNEMONIC = 2;
  public static final int MNEMONICO = 4;
  public static final int ARGUMENTS = 6;
  public static final int PREPROC = 8;
  public static final int PRAGMA = 10;
  public static final int TLIT = 12;
  public static final int FLIT = 14;

  /**
   * ZZ_LEXSTATE[l] is the state in the DFA for the lexical state l
   * ZZ_LEXSTATE[l+1] is the state in the DFA for the lexical state l
   *                  at the beginning of a line
   * l is of the form l = 2*k, k a non negative integer
   */
  private static final int ZZ_LEXSTATE[] = { 
     0,  0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7, 7
  };

  /** 
   * Translates characters to character classes
   * Chosen bits are [7, 7, 7]
   * Total runtime size is 1672 bytes
   */
  public static int ZZ_CMAP(int ch) {
    return ZZ_CMAP_A[(ZZ_CMAP_Y[ZZ_CMAP_Z[ch>>14]|((ch>>7)&0x7f)]<<7)|(ch&0x7f)];
  }

  /* The ZZ_CMAP_Z table has 68 entries */
  static final char ZZ_CMAP_Z[] = zzUnpackCMap(
    "\1\0\103\200");

  /* The ZZ_CMAP_Y table has 256 entries */
  static final char ZZ_CMAP_Y[] = zzUnpackCMap(
    "\1\0\1\1\1\2\77\1\1\3\275\1");

  /* The ZZ_CMAP_A table has 512 entries */
  static final char ZZ_CMAP_A[] = zzUnpackCMap(
    "\11\0\1\40\1\65\2\0\1\43\22\0\1\64\1\51\1\63\1\41\1\72\2\61\1\62\1\71\1\60"+
    "\1\42\1\67\1\47\1\50\1\33\1\61\1\54\1\55\4\56\4\34\1\45\1\44\1\0\1\46\1\53"+
    "\1\0\1\66\1\1\1\2\1\3\1\24\1\12\1\30\1\14\1\16\1\36\1\11\1\37\1\17\1\4\1\21"+
    "\1\5\1\20\1\13\1\23\1\35\1\15\1\32\1\6\1\25\1\22\1\31\1\10\3\0\1\61\1\52\1"+
    "\0\1\1\1\2\1\3\1\24\1\12\1\30\1\14\1\16\1\36\1\11\1\37\1\17\1\4\1\21\1\5\1"+
    "\20\1\13\1\23\1\35\1\15\1\32\1\6\1\25\1\22\1\31\1\10\1\0\1\57\1\0\1\70\261"+
    "\0\2\26\115\0\1\7\52\0\1\27\125\0");

  /** 
   * Translates DFA states to action switch labels.
   */
  private static final int [] ZZ_ACTION = zzUnpackAction();

  private static final String ZZ_ACTION_PACKED_0 =
    "\10\0\1\1\1\2\1\3\1\4\1\5\1\6\1\7"+
    "\1\2\1\5\1\10\1\11\1\10\2\1\1\10\6\1"+
    "\1\11\7\1\1\12\1\13\3\2\1\14\1\2\1\1"+
    "\1\15\1\1\1\16\1\17\1\1\1\20\1\21\1\22"+
    "\1\23\1\13\1\24\1\25\1\26\1\27\1\30\1\31"+
    "\1\32\2\1\1\33\1\34\1\35\1\36\1\37\1\40"+
    "\1\6\1\41\1\10\1\42\2\0\1\43\3\0\1\11"+
    "\3\0\1\10\12\0\1\10\12\0\2\44\4\0\1\44"+
    "\11\0\1\43\11\0\1\45\12\0\1\46\1\47\1\50"+
    "\1\51\1\52\1\51\1\53\1\54\2\14\1\0\1\55"+
    "\1\0\1\11\3\0\1\56\5\0\1\57\4\0\1\10"+
    "\1\60\5\0\1\61\1\62\1\61\3\0\1\63\1\64"+
    "\2\0\1\65\1\0\1\65\3\0\1\66\1\0\1\45"+
    "\1\67\1\57\2\0\1\70\1\71\3\0\1\11\1\0"+
    "\1\72\2\0\1\73\1\0\1\74\1\75\1\76\1\77"+
    "\1\100\1\101\1\102\1\103\1\104\1\105\1\106\1\107"+
    "\1\110\1\111\1\0\1\112";

  private static int [] zzUnpackAction() {
    int [] result = new int[229];
    int offset = 0;
    offset = zzUnpackAction(ZZ_ACTION_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackAction(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }


  /** 
   * Translates a state to a row index in the transition table
   */
  private static final int [] ZZ_ROWMAP = zzUnpackRowMap();

  private static final String ZZ_ROWMAP_PACKED_0 =
    "\0\0\0\73\0\166\0\261\0\354\0\u0127\0\u0162\0\u019d"+
    "\0\u01d8\0\u0213\0\u024e\0\u0289\0\u02c4\0\u02ff\0\u01d8\0\u033a"+
    "\0\u01d8\0\u0375\0\u03b0\0\u03eb\0\u0426\0\u0461\0\u049c\0\u04d7"+
    "\0\u0512\0\u054d\0\u0588\0\u05c3\0\u05fe\0\u0639\0\u0674\0\u06af"+
    "\0\u06ea\0\u0725\0\u0760\0\u079b\0\u07d6\0\u0811\0\u084c\0\u0887"+
    "\0\u08c2\0\u08fd\0\u0938\0\u0973\0\u09ae\0\u01d8\0\u09e9\0\u01d8"+
    "\0\u01d8\0\u0a24\0\u01d8\0\u01d8\0\u01d8\0\u01d8\0\u0a5f\0\u01d8"+
    "\0\u01d8\0\u01d8\0\u01d8\0\u01d8\0\u0a9a\0\u01d8\0\u0ad5\0\u0b10"+
    "\0\u01d8\0\u01d8\0\u0b4b\0\u0b86\0\u0bc1\0\u01d8\0\u0bfc\0\u0bfc"+
    "\0\u0c37\0\u01d8\0\u0c72\0\u0cad\0\u01d8\0\u0ce8\0\u0d23\0\u0d5e"+
    "\0\u0d99\0\u0dd4\0\u0e0f\0\u0e4a\0\u01d8\0\u0e85\0\u0ec0\0\u0efb"+
    "\0\u0f36\0\u0f71\0\u0fac\0\u0fe7\0\u1022\0\u105d\0\u1098\0\u10d3"+
    "\0\u110e\0\u1149\0\u1184\0\u11bf\0\u11fa\0\u1235\0\u1270\0\u12ab"+
    "\0\u12e6\0\u1321\0\u135c\0\u1397\0\u13d2\0\u140d\0\u1448\0\u1483"+
    "\0\u01d8\0\u14be\0\u14f9\0\u1534\0\u156f\0\u15aa\0\u15e5\0\u1620"+
    "\0\u165b\0\u1696\0\u16d1\0\u170c\0\u1747\0\u1782\0\u17bd\0\u17f8"+
    "\0\u1833\0\u186e\0\u18a9\0\u18e4\0\u191f\0\u195a\0\u1995\0\u19d0"+
    "\0\u1a0b\0\u1a46\0\u1a81\0\u1abc\0\u1af7\0\u1b32\0\u1b6d\0\u07d6"+
    "\0\u01d8\0\u01d8\0\u0213\0\u0213\0\u1ba8\0\u01d8\0\u09ae\0\u09e9"+
    "\0\u0a24\0\u1be3\0\u01d8\0\u0b86\0\u01d8\0\u1c1e\0\u1c59\0\u1c94"+
    "\0\u01d8\0\u1ccf\0\u1d0a\0\u1d45\0\u1d80\0\u1dbb\0\u01d8\0\u1df6"+
    "\0\u1e31\0\u1e6c\0\u1ea7\0\u1ee2\0\u1f1d\0\u1f58\0\u1f93\0\u1fce"+
    "\0\u2009\0\u2044\0\u207f\0\u01d8\0\u01d8\0\u20ba\0\u20f5\0\u2130"+
    "\0\u01d8\0\u01d8\0\u216b\0\u21a6\0\u01d8\0\u21e1\0\u221c\0\u221c"+
    "\0\u2257\0\u2292\0\u01d8\0\u22cd\0\u01d8\0\u01d8\0\u2308\0\u2343"+
    "\0\u237e\0\u01d8\0\u01d8\0\u23b9\0\u23f4\0\u2308\0\u242f\0\u246a"+
    "\0\u01d8\0\u24a5\0\u24e0\0\u01d8\0\u251b\0\u01d8\0\u01d8\0\u01d8"+
    "\0\u01d8\0\u01d8\0\u01d8\0\u01d8\0\u01d8\0\u01d8\0\u01d8\0\u01d8"+
    "\0\u01d8\0\u01d8\0\u01d8\0\u2556\0\u2556";

  private static int [] zzUnpackRowMap() {
    int [] result = new int[229];
    int offset = 0;
    offset = zzUnpackRowMap(ZZ_ROWMAP_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackRowMap(String packed, int offset, int [] result) {
    int i = 0;  /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int high = packed.charAt(i++) << 16;
      result[j++] = high | packed.charAt(i++);
    }
    return j;
  }

  /** 
   * The transition table of the DFA
   */
  private static final int [] ZZ_TRANS = zzUnpackTrans();

  private static final String ZZ_TRANS_PACKED_0 =
    "\1\11\6\12\1\11\16\12\2\11\3\12\2\11\3\12"+
    "\1\13\1\11\1\14\1\15\1\16\1\17\3\11\1\20"+
    "\1\12\11\11\1\13\1\21\6\11\1\22\1\23\1\24"+
    "\1\25\1\26\1\11\1\27\1\11\1\30\1\31\2\11"+
    "\1\32\1\11\1\33\1\34\1\35\1\36\1\37\1\40"+
    "\1\41\1\42\1\11\1\43\1\11\1\44\1\45\1\11"+
    "\1\27\1\42\1\11\1\46\2\11\1\15\1\16\17\11"+
    "\1\46\1\21\45\11\1\47\2\11\1\15\1\16\17\11"+
    "\1\47\1\21\6\11\1\12\1\50\4\12\1\11\12\12"+
    "\1\51\1\52\1\12\1\50\2\11\3\12\1\11\1\53"+
    "\1\54\2\12\1\11\1\55\1\56\1\15\1\16\1\57"+
    "\1\11\1\60\1\61\1\20\1\12\1\62\3\53\1\63"+
    "\1\64\1\63\1\65\1\66\1\67\1\21\1\70\1\71"+
    "\1\72\1\73\1\74\40\75\1\11\2\75\1\15\1\16"+
    "\2\75\1\76\14\75\1\67\1\21\5\75\1\11\1\77"+
    "\22\11\1\100\10\11\1\100\2\11\1\47\2\11\1\15"+
    "\1\16\1\11\1\101\1\102\14\11\1\47\1\21\5\11"+
    "\43\103\1\15\1\16\15\103\1\104\2\103\1\21\5\103"+
    "\43\105\1\15\1\16\16\105\1\106\1\105\1\21\5\105"+
    "\73\0\40\12\4\0\1\12\1\0\1\12\3\0\6\12"+
    "\6\0\1\12\3\0\1\12\40\0\1\13\23\0\1\13"+
    "\6\0\43\14\1\0\21\14\1\0\5\14\65\0\1\21"+
    "\5\0\43\107\1\0\1\107\1\110\17\107\1\0\5\107"+
    "\40\12\4\0\1\12\1\0\1\12\2\0\1\20\6\12"+
    "\6\0\1\12\3\0\1\12\2\0\1\111\1\0\1\112"+
    "\1\113\13\0\1\114\4\0\1\115\7\0\1\115\35\0"+
    "\1\116\1\0\1\117\3\0\1\120\2\0\1\120\4\0"+
    "\1\121\6\0\1\122\2\0\1\123\3\0\1\120\1\122"+
    "\35\0\1\124\1\125\2\0\1\126\1\0\1\127\1\130"+
    "\1\0\1\131\4\0\1\132\6\0\1\115\1\133\5\0"+
    "\1\127\1\115\1\133\40\0\1\134\12\0\1\135\75\0"+
    "\1\136\50\0\1\137\1\140\1\0\1\112\1\141\2\0"+
    "\1\141\1\0\1\142\2\0\1\143\1\0\1\144\3\0"+
    "\1\145\1\0\1\146\51\0\1\147\1\150\4\0\1\151"+
    "\1\0\1\152\1\0\1\153\1\154\1\0\1\155\57\0"+
    "\1\156\4\0\1\157\5\0\1\160\53\0\1\161\1\162"+
    "\1\163\2\0\1\162\2\0\1\164\13\0\1\165\6\0"+
    "\1\162\1\165\41\0\1\166\1\0\1\167\13\0\1\170"+
    "\1\171\1\172\1\173\6\0\1\167\1\173\35\0\1\174"+
    "\3\0\1\175\1\0\1\127\2\0\1\131\13\0\1\176"+
    "\3\0\1\177\2\0\1\127\1\176\41\0\1\200\4\0"+
    "\1\201\65\0\1\202\72\0\1\113\1\0\1\203\2\0"+
    "\1\204\2\0\1\205\17\0\1\203\36\0\1\206\3\0"+
    "\1\207\1\0\1\127\2\0\1\210\7\0\1\211\3\0"+
    "\1\212\6\0\1\127\1\212\46\0\1\213\101\0\1\214"+
    "\2\0\1\215\65\0\1\216\74\0\1\217\52\0\6\220"+
    "\1\0\16\220\2\0\3\220\1\0\4\220\14\0\3\220"+
    "\54\0\1\46\23\0\1\46\46\0\1\47\23\0\1\47"+
    "\6\0\40\12\1\0\1\221\2\0\1\12\1\0\1\12"+
    "\3\0\6\12\6\0\1\12\3\0\41\12\1\0\1\222"+
    "\2\0\1\12\1\0\1\12\3\0\6\12\6\0\1\12"+
    "\3\0\35\12\1\223\3\12\4\0\1\12\1\0\1\12"+
    "\3\0\2\12\1\224\1\225\1\223\1\12\6\0\1\12"+
    "\3\0\1\12\34\0\1\53\17\0\3\53\14\0\40\12"+
    "\1\0\1\226\2\0\1\12\1\0\1\12\3\0\6\12"+
    "\6\0\1\12\3\0\1\12\34\0\1\227\17\0\3\227"+
    "\70\0\2\230\16\0\3\231\6\0\1\231\11\0\1\231"+
    "\3\0\1\231\3\0\1\231\17\0\3\231\100\0\1\67"+
    "\6\0\40\75\1\0\2\75\1\0\3\75\1\0\14\75"+
    "\2\0\5\75\17\0\1\232\123\0\1\233\16\0\1\233"+
    "\3\0\43\103\1\0\16\103\1\234\2\103\1\0\5\103"+
    "\62\0\1\103\10\0\43\105\1\0\17\105\1\0\1\105"+
    "\1\0\5\105\43\107\1\0\21\107\1\0\5\107\7\0"+
    "\1\235\25\0\1\235\60\0\1\236\73\0\1\136\67\0"+
    "\1\237\56\0\1\240\74\0\1\241\25\0\1\241\44\0"+
    "\1\242\15\0\1\243\7\0\1\242\56\0\1\244\66\0"+
    "\1\245\74\0\1\246\56\0\1\247\14\0\1\250\64\0"+
    "\1\251\63\0\1\247\110\0\1\252\74\0\1\235\54\0"+
    "\1\253\73\0\1\254\115\0\1\255\67\0\1\115\7\0"+
    "\1\115\42\0\1\245\71\0\1\161\2\0\1\161\65\0"+
    "\1\254\104\0\1\256\60\0\1\257\3\0\1\260\13\0"+
    "\1\261\1\0\1\262\7\0\1\260\36\0\1\263\1\0"+
    "\1\264\70\0\1\263\1\0\1\265\6\0\1\266\4\0"+
    "\1\265\73\0\1\267\72\0\1\161\55\0\1\161\14\0"+
    "\1\161\65\0\1\161\74\0\1\161\67\0\1\161\72\0"+
    "\1\161\2\0\1\161\60\0\1\161\1\0\1\161\4\0"+
    "\1\161\72\0\1\270\112\0\1\241\64\0\1\271\52\0"+
    "\1\163\70\0\1\272\112\0\1\273\65\0\1\274\56\0"+
    "\1\252\106\0\1\275\67\0\1\276\63\0\1\257\107\0"+
    "\1\277\56\0\1\300\2\0\1\301\25\0\1\301\51\0"+
    "\1\302\76\0\1\303\74\0\1\264\57\0\1\304\25\0"+
    "\1\304\55\0\1\305\66\0\1\235\76\0\1\306\2\0"+
    "\1\307\61\0\1\310\73\0\1\311\1\0\1\312\12\0"+
    "\1\313\67\0\1\314\62\0\1\315\100\0\1\316\52\0"+
    "\1\317\15\0\1\252\6\0\1\271\47\0\1\320\73\0"+
    "\1\255\77\0\1\157\62\0\1\317\2\0\1\235\101\0"+
    "\1\321\1\0\1\322\60\0\1\323\104\0\1\324\53\0"+
    "\40\12\4\0\1\12\1\0\1\12\3\0\2\12\3\223"+
    "\1\12\6\0\1\12\3\0\1\12\20\0\1\325\66\0"+
    "\1\326\105\0\1\241\7\0\1\241\53\0\1\250\101\0"+
    "\1\327\7\0\1\327\53\0\1\235\76\0\1\330\60\0"+
    "\1\331\77\0\1\303\104\0\1\332\55\0\1\333\102\0"+
    "\1\333\67\0\1\334\6\0\1\334\44\0\1\125\77\0"+
    "\1\335\25\0\1\335\42\0\1\235\110\0\1\336\64\0"+
    "\1\337\103\0\1\340\7\0\1\340\54\0\1\337\56\0"+
    "\1\272\116\0\1\333\44\0\1\235\111\0\1\324\66\0"+
    "\1\340\74\0\1\321\75\0\1\334\76\0\1\341\7\0"+
    "\1\341\51\0\1\324\67\0\1\324\76\0\1\303\70\0"+
    "\1\241\73\0\1\334\107\0\1\342\60\0\1\334\53\0"+
    "\1\331\106\0\1\235\75\0\1\324\64\0\1\334\61\0"+
    "\1\343\107\0\1\344\55\0\1\345\71\0";

  private static int [] zzUnpackTrans() {
    int [] result = new int[9617];
    int offset = 0;
    offset = zzUnpackTrans(ZZ_TRANS_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackTrans(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      value--;
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }


  /* error codes */
  private static final int ZZ_UNKNOWN_ERROR = 0;
  private static final int ZZ_NO_MATCH = 1;
  private static final int ZZ_PUSHBACK_2BIG = 2;

  /* error messages for the codes above */
  private static final String[] ZZ_ERROR_MSG = {
    "Unknown internal scanner error",
    "Error: could not match input",
    "Error: pushback value was too large"
  };

  /**
   * ZZ_ATTRIBUTE[aState] contains the attributes of state <code>aState</code>
   */
  private static final int [] ZZ_ATTRIBUTE = zzUnpackAttribute();

  private static final String ZZ_ATTRIBUTE_PACKED_0 =
    "\10\0\1\11\5\1\1\11\1\1\1\11\34\1\1\11"+
    "\1\1\2\11\1\1\4\11\1\1\5\11\1\1\1\11"+
    "\2\1\2\11\3\1\1\11\3\1\1\11\2\0\1\11"+
    "\3\0\1\1\3\0\1\11\12\0\1\1\12\0\2\1"+
    "\4\0\1\11\11\0\1\1\11\0\1\1\12\0\1\1"+
    "\2\11\3\1\1\11\3\1\1\0\1\11\1\0\1\11"+
    "\3\0\1\11\5\0\1\11\4\0\2\1\5\0\1\1"+
    "\2\11\3\0\2\11\2\0\1\11\1\0\1\1\3\0"+
    "\1\11\1\0\2\11\1\1\2\0\2\11\3\0\1\1"+
    "\1\0\1\11\2\0\1\11\1\0\16\11\1\0\1\1";

  private static int [] zzUnpackAttribute() {
    int [] result = new int[229];
    int offset = 0;
    offset = zzUnpackAttribute(ZZ_ATTRIBUTE_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackAttribute(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }

  /** the input device */
  private java.io.Reader zzReader;

  /** the current state of the DFA */
  private int zzState;

  /** the current lexical state */
  private int zzLexicalState = YYINITIAL;

  /** this buffer contains the current text to be matched and is
      the source of the yytext() string */
  private CharSequence zzBuffer = "";

  /** the textposition at the last accepting state */
  private int zzMarkedPos;

  /** the current text position in the buffer */
  private int zzCurrentPos;

  /** startRead marks the beginning of the yytext() string in the buffer */
  private int zzStartRead;

  /** endRead marks the last character in the buffer, that has been read
      from input */
  private int zzEndRead;

  /**
   * zzAtBOL == true <=> the scanner is currently at the beginning of a line
   */
  private boolean zzAtBOL = true;

  /** zzAtEOF == true <=> the scanner is at the EOF */
  private boolean zzAtEOF;

  /** denotes if the user-EOF-code has already been executed */
  private boolean zzEOFDone;


  /**
   * Creates a new scanner
   *
   * @param   in  the java.io.Reader to read input from.
   */
  Xas99RLexer(java.io.Reader in) {
    this.zzReader = in;
  }


  /** 
   * Unpacks the compressed character translation table.
   *
   * @param packed   the packed character translation table
   * @return         the unpacked character translation table
   */
  private static char [] zzUnpackCMap(String packed) {
    int size = 0;
    for (int i = 0, length = packed.length(); i < length; i += 2) {
      size += packed.charAt(i);
    }
    char[] map = new char[size];
    int i = 0;  /* index in packed string  */
    int j = 0;  /* index in unpacked array */
    while (i < packed.length()) {
      int  count = packed.charAt(i++);
      char value = packed.charAt(i++);
      do map[j++] = value; while (--count > 0);
    }
    return map;
  }

  public final int getTokenStart() {
    return zzStartRead;
  }

  public final int getTokenEnd() {
    return getTokenStart() + yylength();
  }

  public void reset(CharSequence buffer, int start, int end, int initialState) {
    zzBuffer = buffer;
    zzCurrentPos = zzMarkedPos = zzStartRead = start;
    zzAtEOF  = false;
    zzAtBOL = true;
    zzEndRead = end;
    yybegin(initialState);
  }

  /**
   * Refills the input buffer.
   *
   * @return      {@code false}, iff there was new input.
   *
   * @exception   java.io.IOException  if any I/O-Error occurs
   */
  private boolean zzRefill() throws java.io.IOException {
    return true;
  }


  /**
   * Returns the current lexical state.
   */
  public final int yystate() {
    return zzLexicalState;
  }


  /**
   * Enters a new lexical state
   *
   * @param newState the new lexical state
   */
  public final void yybegin(int newState) {
    zzLexicalState = newState;
  }


  /**
   * Returns the text matched by the current regular expression.
   */
  public final CharSequence yytext() {
    return zzBuffer.subSequence(zzStartRead, zzMarkedPos);
  }


  /**
   * Returns the character at position {@code pos} from the
   * matched text.
   *
   * It is equivalent to yytext().charAt(pos), but faster
   *
   * @param pos the position of the character to fetch.
   *            A value from 0 to yylength()-1.
   *
   * @return the character at position pos
   */
  public final char yycharat(int pos) {
    return zzBuffer.charAt(zzStartRead+pos);
  }


  /**
   * Returns the length of the matched text region.
   */
  public final int yylength() {
    return zzMarkedPos-zzStartRead;
  }


  /**
   * Reports an error that occurred while scanning.
   *
   * In a wellformed scanner (no or only correct usage of
   * yypushback(int) and a match-all fallback rule) this method
   * will only be called with things that "Can't Possibly Happen".
   * If this method is called, something is seriously wrong
   * (e.g. a JFlex bug producing a faulty scanner etc.).
   *
   * Usual syntax/scanner level error handling should be done
   * in error fallback rules.
   *
   * @param   errorCode  the code of the errormessage to display
   */
  private void zzScanError(int errorCode) {
    String message;
    try {
      message = ZZ_ERROR_MSG[errorCode];
    }
    catch (ArrayIndexOutOfBoundsException e) {
      message = ZZ_ERROR_MSG[ZZ_UNKNOWN_ERROR];
    }

    throw new Error(message);
  }


  /**
   * Pushes the specified amount of characters back into the input stream.
   *
   * They will be read again by then next call of the scanning method
   *
   * @param number  the number of characters to be read again.
   *                This number must not be greater than yylength()!
   */
  public void yypushback(int number)  {
    if ( number > yylength() )
      zzScanError(ZZ_PUSHBACK_2BIG);

    zzMarkedPos -= number;
  }


  /**
   * Contains user EOF-code, which will be executed exactly once,
   * when the end of file is reached
   */
  private void zzDoEOF() {
    if (!zzEOFDone) {
      zzEOFDone = true;
    
    }
  }


  /**
   * Resumes scanning until the next regular expression is matched,
   * the end of input is encountered or an I/O-Error occurs.
   *
   * @return      the next token
   * @exception   java.io.IOException  if any I/O-Error occurs
   */
  public IElementType advance() throws java.io.IOException {
    int zzInput;
    int zzAction;

    // cached fields:
    int zzCurrentPosL;
    int zzMarkedPosL;
    int zzEndReadL = zzEndRead;
    CharSequence zzBufferL = zzBuffer;

    int [] zzTransL = ZZ_TRANS;
    int [] zzRowMapL = ZZ_ROWMAP;
    int [] zzAttrL = ZZ_ATTRIBUTE;

    while (true) {
      zzMarkedPosL = zzMarkedPos;

      zzAction = -1;

      zzCurrentPosL = zzCurrentPos = zzStartRead = zzMarkedPosL;

      zzState = ZZ_LEXSTATE[zzLexicalState];

      // set up zzAction for empty match case:
      int zzAttributes = zzAttrL[zzState];
      if ( (zzAttributes & 1) == 1 ) {
        zzAction = zzState;
      }


      zzForAction: {
        while (true) {

          if (zzCurrentPosL < zzEndReadL) {
            zzInput = Character.codePointAt(zzBufferL, zzCurrentPosL/*, zzEndReadL*/);
            zzCurrentPosL += Character.charCount(zzInput);
          }
          else if (zzAtEOF) {
            zzInput = YYEOF;
            break zzForAction;
          }
          else {
            // store back cached positions
            zzCurrentPos  = zzCurrentPosL;
            zzMarkedPos   = zzMarkedPosL;
            boolean eof = zzRefill();
            // get translated positions and possibly new buffer
            zzCurrentPosL  = zzCurrentPos;
            zzMarkedPosL   = zzMarkedPos;
            zzBufferL      = zzBuffer;
            zzEndReadL     = zzEndRead;
            if (eof) {
              zzInput = YYEOF;
              break zzForAction;
            }
            else {
              zzInput = Character.codePointAt(zzBufferL, zzCurrentPosL/*, zzEndReadL*/);
              zzCurrentPosL += Character.charCount(zzInput);
            }
          }
          int zzNext = zzTransL[ zzRowMapL[zzState] + ZZ_CMAP(zzInput) ];
          if (zzNext == -1) break zzForAction;
          zzState = zzNext;

          zzAttributes = zzAttrL[zzState];
          if ( (zzAttributes & 1) == 1 ) {
            zzAction = zzState;
            zzMarkedPosL = zzCurrentPosL;
            if ( (zzAttributes & 8) == 8 ) break zzForAction;
          }

        }
      }

      // store back cached position
      zzMarkedPos = zzMarkedPosL;

      if (zzInput == YYEOF && zzStartRead == zzCurrentPos) {
        zzAtEOF = true;
        zzDoEOF();
        return null;
      }
      else {
        switch (zzAction < 0 ? zzAction : ZZ_ACTION[zzAction]) {
          case 1: 
            { return TokenType.BAD_CHARACTER;
            } 
            // fall through
          case 75: break;
          case 2: 
            { return Xas99RTypes.IDENT;
            } 
            // fall through
          case 76: break;
          case 3: 
            { yybegin(MNEMONIC); return TokenType.WHITE_SPACE;
            } 
            // fall through
          case 77: break;
          case 4: 
            { return Xas99RTypes.LCOMMENT;
            } 
            // fall through
          case 78: break;
          case 5: 
            { yybegin(YYINITIAL); return Xas99RTypes.CRLF;
            } 
            // fall through
          case 79: break;
          case 6: 
            { return Xas99RTypes.COMMENT;
            } 
            // fall through
          case 80: break;
          case 7: 
            { return Xas99RTypes.OP_COLON;
            } 
            // fall through
          case 81: break;
          case 8: 
            { return Xas99RTypes.INSTR_I;
            } 
            // fall through
          case 82: break;
          case 9: 
            { return Xas99RTypes.INSTR_VI;
            } 
            // fall through
          case 83: break;
          case 10: 
            { yybegin(ARGUMENTS); return TokenType.WHITE_SPACE;
            } 
            // fall through
          case 84: break;
          case 11: 
            { return TokenType.WHITE_SPACE;
            } 
            // fall through
          case 85: break;
          case 12: 
            { return Xas99RTypes.INT;
            } 
            // fall through
          case 86: break;
          case 13: 
            { return Xas99RTypes.OP_AST;
            } 
            // fall through
          case 87: break;
          case 14: 
            { return Xas99RTypes.OP_SEP;
            } 
            // fall through
          case 88: break;
          case 15: 
            { return Xas99RTypes.OP_MINUS;
            } 
            // fall through
          case 89: break;
          case 16: 
            { return Xas99RTypes.OP_MISC;
            } 
            // fall through
          case 90: break;
          case 17: 
            { return Xas99RTypes.OP_RPAREN;
            } 
            // fall through
          case 91: break;
          case 18: 
            { yybegin(TLIT); return Xas99RTypes.OP_QUOTE;
            } 
            // fall through
          case 92: break;
          case 19: 
            { yybegin(FLIT); return Xas99RTypes.OP_FQUOTE;
            } 
            // fall through
          case 93: break;
          case 20: 
            { return Xas99RTypes.OP_AT;
            } 
            // fall through
          case 94: break;
          case 21: 
            { return Xas99RTypes.OP_PLUS;
            } 
            // fall through
          case 95: break;
          case 22: 
            { return Xas99RTypes.OP_NOT;
            } 
            // fall through
          case 96: break;
          case 23: 
            { return Xas99RTypes.OP_LPAREN;
            } 
            // fall through
          case 97: break;
          case 24: 
            { return Xas99RTypes.OP_LC;
            } 
            // fall through
          case 98: break;
          case 25: 
            { return Xas99RTypes.PP_ARG;
            } 
            // fall through
          case 99: break;
          case 26: 
            { return Xas99RTypes.PP_SEP;
            } 
            // fall through
          case 100: break;
          case 27: 
            { return Xas99RTypes.PG_EQ;
            } 
            // fall through
          case 101: break;
          case 28: 
            { return Xas99RTypes.PG_SEP;
            } 
            // fall through
          case 102: break;
          case 29: 
            { return Xas99RTypes.TEXT;
            } 
            // fall through
          case 103: break;
          case 30: 
            { yybegin(ARGUMENTS); return Xas99RTypes.OP_QUOTE;
            } 
            // fall through
          case 104: break;
          case 31: 
            { return Xas99RTypes.FNAME;
            } 
            // fall through
          case 105: break;
          case 32: 
            { yybegin(ARGUMENTS); return Xas99RTypes.OP_FQUOTE;
            } 
            // fall through
          case 106: break;
          case 33: 
            { yybegin(PRAGMA); return Xas99RTypes.PG_START;
            } 
            // fall through
          case 107: break;
          case 34: 
            { return Xas99RTypes.INSTR_99000_I;
            } 
            // fall through
          case 108: break;
          case 35: 
            { return Xas99RTypes.INSTR_VIII;
            } 
            // fall through
          case 109: break;
          case 36: 
            { return Xas99RTypes.INSTR_II;
            } 
            // fall through
          case 110: break;
          case 37: 
            { yybegin(MNEMONICO); return Xas99RTypes.INSTR_O;
            } 
            // fall through
          case 111: break;
          case 38: 
            { yybegin(PREPROC); return Xas99RTypes.PREP;
            } 
            // fall through
          case 112: break;
          case 39: 
            { return Xas99RTypes.MOD_AUTO;
            } 
            // fall through
          case 113: break;
          case 40: 
            { return Xas99RTypes.MOD_XBANK;
            } 
            // fall through
          case 114: break;
          case 41: 
            { return Xas99RTypes.REGISTER;
            } 
            // fall through
          case 115: break;
          case 42: 
            { return Xas99RTypes.REGISTER0;
            } 
            // fall through
          case 116: break;
          case 43: 
            { return Xas99RTypes.MOD_LEN;
            } 
            // fall through
          case 117: break;
          case 44: 
            { return Xas99RTypes.PP_PARAM;
            } 
            // fall through
          case 118: break;
          case 45: 
            { return Xas99RTypes.PG_CYC;
            } 
            // fall through
          case 119: break;
          case 46: 
            { return Xas99RTypes.DIR_E;
            } 
            // fall through
          case 120: break;
          case 47: 
            { return Xas99RTypes.INSTR_III;
            } 
            // fall through
          case 121: break;
          case 48: 
            { return Xas99RTypes.INSTR_IX;
            } 
            // fall through
          case 122: break;
          case 49: 
            { return Xas99RTypes.INSTR_V;
            } 
            // fall through
          case 123: break;
          case 50: 
            { return Xas99RTypes.INSTR_F18A_IA;
            } 
            // fall through
          case 124: break;
          case 51: 
            { return Xas99RTypes.DIR_L;
            } 
            // fall through
          case 125: break;
          case 52: 
            { return Xas99RTypes.INSTR_99000_IV;
            } 
            // fall through
          case 126: break;
          case 53: 
            { return Xas99RTypes.INSTR_9995_VIII;
            } 
            // fall through
          case 127: break;
          case 54: 
            { return Xas99RTypes.INSTR_F18A_VI;
            } 
            // fall through
          case 128: break;
          case 55: 
            { return Xas99RTypes.INSTR_IX_X;
            } 
            // fall through
          case 129: break;
          case 56: 
            { yybegin(MNEMONICO); return Xas99RTypes.INSTR_F18A_O;
            } 
            // fall through
          case 130: break;
          case 57: 
            { return Xas99RTypes.DIR_R;
            } 
            // fall through
          case 131: break;
          case 58: 
            { return Xas99RTypes.DIR_S;
            } 
            // fall through
          case 132: break;
          case 59: 
            { yybegin(MNEMONICO); return Xas99RTypes.DIR_O;
            } 
            // fall through
          case 133: break;
          case 60: 
            { return Xas99RTypes.DIR_EO;
            } 
            // fall through
          case 134: break;
          case 61: 
            { return Xas99RTypes.INSTR_99000_VIII;
            } 
            // fall through
          case 135: break;
          case 62: 
            { return Xas99RTypes.INSTR_99000_VI;
            } 
            // fall through
          case 136: break;
          case 63: 
            { return Xas99RTypes.DIR_ES;
            } 
            // fall through
          case 137: break;
          case 64: 
            { return Xas99RTypes.DIR_C;
            } 
            // fall through
          case 138: break;
          case 65: 
            { yybegin(MNEMONICO); return Xas99RTypes.DIR_X;
            } 
            // fall through
          case 139: break;
          case 66: 
            { yybegin(MNEMONICO); return Xas99RTypes.INSTR_VII;
            } 
            // fall through
          case 140: break;
          case 67: 
            { return Xas99RTypes.INSTR_9995_VI;
            } 
            // fall through
          case 141: break;
          case 68: 
            { return Xas99RTypes.INSTR_IV;
            } 
            // fall through
          case 142: break;
          case 69: 
            { return Xas99RTypes.INSTR_VIII_R;
            } 
            // fall through
          case 143: break;
          case 70: 
            { return Xas99RTypes.DIR_T;
            } 
            // fall through
          case 144: break;
          case 71: 
            { return Xas99RTypes.INSTR_VIII_I;
            } 
            // fall through
          case 145: break;
          case 72: 
            { return Xas99RTypes.DIR_RA;
            } 
            // fall through
          case 146: break;
          case 73: 
            { return Xas99RTypes.DIR_F;
            } 
            // fall through
          case 147: break;
          case 74: 
            { return Xas99RTypes.PG_TERM;
            } 
            // fall through
          case 148: break;
          default:
            zzScanError(ZZ_NO_MATCH);
          }
      }
    }
  }


}